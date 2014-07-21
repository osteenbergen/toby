define([
    'require',
    'angular',
    //Require our application
    './toby',
], function (require, ng) {
    'use strict';
    
    //When the dom is ready, initialize our application
    require(['domReady!'], function (document) {
        ng.bootstrap(document, ['toby']);
    });
});
