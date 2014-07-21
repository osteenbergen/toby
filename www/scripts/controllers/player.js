define([
        './controllers'
    ],function(controllers){
        controllers.controller('PlayerCtrl',[
            '$scope',
            '$http',
            '$location',
            'Status',
            function($scope, $http, $location, Status){
                $scope.init = true
                //TODO: Should be a service
                $scope.call = function(action, callback){
                        $http({
                            method: 'Get',
                            url: '/player/' + action 
                        }).
                        success(function(data, status, headers, config){
                            if(callback)
                                callback(data);
                        }).
                        error(function(data, status, headers, config){
                            console.log("Error");
                        });

	            }
                $scope.sync = function(){
                    //If we are not streaming the player will not work
                    if(!Status.get_stream()){
                        $location.path('/torrent');
                    } else if($scope.init) {
                        //Should we open the player window?
                        $scope.call('open', function(data){
                            $scope.init = !data.status;
                        });
                    }
                }
                $scope.play = function(){
                    //Send play to the API
                    $scope.call('play');
                }
                $scope.pause = function(){
                    $scope.call('pause');
                }
                $scope.stop = function(){
                    $scope.call('stop');
                    //Reset everything
                    $scope.init = true;
                    //FIFO, so we also close the stream
                    Status.set_stream(false);
                    $location.path('/torrent');
                }
            }
        ]);
    }
);
