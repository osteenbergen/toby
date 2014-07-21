define([
        './controllers'
    ],function(controllers){
        controllers.controller('TorrentCtrl',[
            '$scope',
            '$http',
            '$location',
            '$timeout',
            'Status',
            function($scope, $http, $location, $timeout, Status){
                $scope.init = true
                $scope.info = false
                //TODO: Should be a service
                $scope.call = function(url, callback){
                    $http({
                        method: 'Get',
                        url: url
                    }).
                    success(function(data, status, headers, config){
                        console.log("Success", data, status);
                        if(data.status !== false)
                            callback(data);
                    }).
                    error(function(data, status, headers, config){
                        console.log("Error");
                    });

                }
                $scope.sync = function(){
                    $scope.call('/torrent/info', function(data){
                        $scope.init = false;
                        $scope.info = data;
                        Status.set_torrent(data.status);
                        if(data.streaming !== null){
                            //Update stream info if needed
                            Status.set_stream(data.streaming);
                        }
                        //Keep asking for data
                        $timeout($scope.sync, 3000);
                    });
                }   
                $scope.load = function(){
                    //Try to load the file
                    //TODO: Error handling
                    $scope.call('/torrent/load/' + 
                                encodeURIComponent($scope.location),
                        function(data){
                            $scope.init = false;
                            $scope.info = data;
                            Status.set_torrent(data.status);
                            $scope.sync()
                    });
                }
                $scope.stop = function(){
                    $scope.call('/torrent/stop', function(data){
                        //Clean up
                        $scope.init = true;
                        $scope.info = false;
                        Status.set_torrent(false);
                        //Show homepage
                        $location.path('/');
                    });
                }
                $scope.stream = function(){
                    //If the stream doesn't exist create a new one
                    //Always open a player
                    if(!Status.get_stream()){
                        $scope.call('/torrent/stream', function(data){
                            Status.set_stream(true);
                            $location.path('/player');
                        });
                    } else {
                        $location.path('/player');
                    }
                }
            }
        ]);
    }
);
