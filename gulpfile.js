// FOLDER PATHS
/***************************************************************************
  File: gulpfile.js
  Description: Defines all the gulp tasks that are needed for UI assets, like
  sass compilation into CSS, or JS minification and bundling.

  Gulp installation commands:
  https://github.com/gulpjs/gulp/blob/master/docs/getting-started.md

  npm install --save-dev gulp-sass
  npm install --save-dev gulp-uglify
  npm install --save-dev gulp-concat
  npm install --save-dev gulp-jshint

****************************************************************************/

'use strict';

// FOLDER PATHS
var sassDir = 'app/static/sass/**/*.scss';
var cssDir = 'app/static/css/';
var sassFolder = 'app/static/sass/**/*.scss';
var jsDir = 'app/static/js/';
var jsBundleDir = 'app/static/js/';

// GULP PLUGINS - must be installed on the machine (see commands above)
var gulp = require('gulp');
var jshint = require('gulp-jshint');
var concat = require('gulp-concat');
var sass = require('gulp-sass');
var minifyCSS = require('gulp-minify-css');
var bundle = require('gulp-bundle-file');
var uglify = require('gulp-uglify');
var runSequence = require('run-sequence');
var rev = require('gulp-rev');
//var browserSync = require('browser-sync');


// GULP TASKS
/**********************************************
 default: runs gulp tasks in the background
**********************************************/
gulp.task('default', ['flask', 'watchsass', 'watchjs']);



/**********************************************
 compilesass: run to compile sass files into css
**********************************************/
gulp.task('compilesass', function() {
    gulp.src(sassDir)
        .pipe(sass().on('error', sass.logError))
        .pipe(sass({outputStyle: 'compressed'}))
        .pipe(gulp.dest(cssDir));
});

gulp.task('watchsass', function() {
  gulp.watch(sassFolder,['compilesass']);
});


/**********************************************
  bundle: run to minify bundle specific js files
**********************************************/
gulp.task('bundles', function() {
    return gulp.src(jsDir + '*.bundle')
        .pipe(bundle.concat()) // concat files in each bundles
        .pipe(uglify())
        .pipe(gulp.dest(jsDir));
});


/**********************************************
  reversion: run to append version has to asset files
  *********************************************/
  gulp.task('reversion', function(){
    return gulp.src(['app/static/css/*.css', 'app/static/js/*.js'], {base:'app/static'})
        .pipe(rev())
        .pipe(gulp.dest('app/static'))
        .pipe(rev.manifest())
        .pipe(gulp.dest('app/static'));

  });


/**********************************************
  jekyll: run to build flask site
**********************************************/
var process = require('child_process');

gulp.task('flask', function(){
  var spawn = process.spawn;
  console.info('Starting flask server');
  var PIPE = {stdio: 'inherit'};
  spawn('python', ['run.py','runserver'], PIPE);
});

gulp.task('watchjs', function() {
  gulp.watch(jsBundleDir,['bundles']);
});


/**********************************************
  build: run to build flask site for production environment
  1. Run Flask
  2. Compile Sass
  3. Bundle JS
  4. Version static assets
**********************************************/
gulp.task('build', function(callback) {
  runSequence('flask',
              'watchsass',
              'bundles',
              'reversion',
              callback);
});

/**********************************************
  build: run to build flask site for development environment
  1. Run Flask
  2. Compile Sass
**********************************************/
gulp.task('dev-build', function(callback) {
  runSequence('flask',
              'watchsass',
              callback);
});
