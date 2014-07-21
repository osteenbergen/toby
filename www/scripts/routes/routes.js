define([
    'angular'
    ],
    function(angular){
        //Create the module
        routes = angular.module('toby.routes',[])
        //Add the default route to the homepage
        routes.config(['$routeProvider',
            function($routeProvider){
                $routeProvider
                    .otherwise({
                        templateUrl: 'views/home.html',
                        controller: 'HomeCtrl'
                    });
            }
        ]);
        return routes
    }
)
