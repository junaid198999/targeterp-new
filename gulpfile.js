////////////////////////////////
//Setup//
////////////////////////////////

// Plugins
var gulp = require('gulp'),
    pjson = require('./package.json'),
    sass = require('gulp-sass'),
    autoprefixer = require('gulp-autoprefixer'),
    cssnano = require('gulp-cssnano'),
    concat = require('gulp-concat'),
    rename = require('gulp-rename'),
    plumber = require('gulp-plumber'),
    pixrem = require('gulp-pixrem'),
    uglify = require('gulp-uglify'),
    imagemin = require('gulp-imagemin'),
    lodash = require("lodash"),
    spawn = require('child_process').spawn,
    browsersync = require('browser-sync').create();


// Relative paths function
var pathsConfig = function (appName) {
    this.app = "./" + (appName || pjson.name);
    var vendorsRoot = 'node_modules/';

    return {
        bootstrapSass: vendorsRoot + '/bootstrap/scss',
        vendorsJs: [
            "./node_modules/jquery/dist/jquery.js",
            "./node_modules/bootstrap/dist/js/bootstrap.bundle.js",
            "./node_modules/metismenu/dist/metisMenu.js",
            "./node_modules/jquery-slimscroll/jquery.slimscroll.js",
            "./node_modules/node-waves/dist/waves.js",
            "./node_modules/waypoints/lib/jquery.waypoints.min.js",
            "./node_modules/jquery.counterup/jquery.counterup.min.js"
        ],
        app: this.app,
        templates: this.app + '/templates',
        css: this.app + '/static/css',
        sass: this.app + '/static/scss',
        fonts: this.app + '/static/fonts',
        images: this.app + '/static/images',
        js: this.app + '/static/js',
        srcJs: this.app + '/static/js/src',
        vendor: this.app + '/static/vendor'
    }
};

var paths = pathsConfig();

////////////////////////////////
//Tasks//
////////////////////////////////

// Styles autoprefixing and minification
function styles() {
    gulp.src(paths.sass + '/bootstrap.scss')
        .pipe(sass({
            includePaths: [
                paths.bootstrapSass,
                paths.sass
            ]
        }).on('error', sass.logError))
        .pipe(plumber()) // Checks for errors
        .pipe(autoprefixer({ overrideBrowserslist: ['last 2 versions'] })) // Adds vendor prefixes
        .pipe(pixrem())  // add fallbacks for rem units
        .pipe(gulp.dest(paths.css))
        .pipe(rename({ suffix: '.min' }))
        .pipe(cssnano()) // Minifies the result
        .pipe(gulp.dest(paths.css));

    gulp.src(paths.sass + '/icons.scss')
        .pipe(sass({
            includePaths: [
                paths.bootstrapSass,
                paths.sass
            ]
        }).on('error', sass.logError))
        .pipe(plumber()) // Checks for errors
        .pipe(autoprefixer({ overrideBrowserslist: ['last 2 versions'] })) // Adds vendor prefixes
        .pipe(pixrem())  // add fallbacks for rem units
        .pipe(gulp.dest(paths.css))
        .pipe(rename({ suffix: '.min' }))
        .pipe(cssnano()) // Minifies the result
        .pipe(gulp.dest(paths.css));

    return gulp.src(paths.sass + '/app.scss')
        .pipe(sass({
            includePaths: [
                paths.bootstrapSass,
                paths.sass
            ]
        }).on('error', sass.logError))
        .pipe(plumber()) // Checks for errors
        .pipe(autoprefixer({ overrideBrowserslist: ['last 2 versions'] })) // Adds vendor prefixes
        .pipe(pixrem())  // add fallbacks for rem units
        .pipe(gulp.dest(paths.css))
        .pipe(rename({ suffix: '.min' }))
        .pipe(cssnano()) // Minifies the result
        .pipe(gulp.dest(paths.css));
}


// Javascript minification
function scripts() {
    var allJs = lodash.union(paths.vendorsJs, [paths.srcJs + '/app.js']);

    return gulp.src(allJs)
        .pipe(concat('app.js'))
        .pipe(gulp.dest(paths.js))
        .pipe(plumber()) // Checks for errors
        .pipe(uglify()) // Minifies the js
        .pipe(rename({ suffix: '.min' }))
        .pipe(gulp.dest(paths.js));
}

// Image compression
function imgCompression() {
    return gulp.src(paths.images + '/*')
        .pipe(imagemin()) // Compresses PNG, JPEG, GIF and SVG images
        .pipe(gulp.dest(paths.images))
}

// Run django server
function runServer(cb) {
    var cmd = spawn('python', ['manage.py', 'runserver'], { stdio: 'inherit' });
    cmd.on('close', function (code) {
        console.log('runServer exited with code ' + code);
        cb(code);
    });
}

// live browser loading
function initBrowserSync(done) {
    browsersync.init({
        proxy: "127.0.0.1:8000"
    });
    done();
}

function reloadBrowserSync(done) {
    browsersync.reload();
    // browsersync.stream({once: true})
    done();
}

function watchFiles() {
    gulp.watch(paths.app + '/**/*.py', gulp.series(reloadBrowserSync));
    gulp.watch(paths.templates + '/**/*', gulp.series(reloadBrowserSync));
    gulp.watch(paths.sass + '/**/*', gulp.series(styles, reloadBrowserSync));
    gulp.watch(paths.js + '/src/**/*', gulp.series(scripts, reloadBrowserSync));
    gulp.watch(paths.images + '/**/*', gulp.series(imgCompression, reloadBrowserSync));
}


var generateAssets = gulp.parallel(
    gulp.series(styles, scripts),
    imgCompression
);

var dev = gulp.parallel(
    runServer,
    initBrowserSync,
    watchFiles
);

exports.default = gulp.series(generateAssets, dev)
exports["build"] = generateAssets
exports["dev"] = dev