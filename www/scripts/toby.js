define([
    'angular',
    'angular_route',
    'angular_resource',
    'angular_bootstrap_tpls',
    'angular_fontawesome',
    'angular_match_media',
    'less',
    //Everything is handled in submodules, the index loads all modules of a specific type
    './controllers/index',
    './routes/index',
    './services/index'
], function(angular) {
    //This is the application and its angularjs dependencies
    var toby = angular.module('toby', [
        'ui.bootstrap',
        'ngMatchMedia',
        'ngRoute',
        'ngResource',
        'picardy.fontawesome',
        'toby.controllers',
        'toby.routes',
        'toby.services'
    ]);
    // Set some configuration options for display
    toby.config(function(devicesProvider){
        devicesProvider.set('big','(min-width:769px)');
        devicesProvider.set('small','(max-width:768px)');
    });
    return toby;
});
