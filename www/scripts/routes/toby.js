define([
    './routes'
    ],
    function(routes){
        routes.config(['$routeProvider',
            //Add some specific routes
            function($routeProvider) {
                $routeProvider
                    .when('/player', {
                        templateUrl: 'views/player.html',
                        controller: 'PlayerCtrl'
                    })
                    .when('/torrent', {
                        templateUrl: 'views/torrent.html',
                        controller: 'TorrentCtrl'
                    })
            }
        ]);
    }
);
