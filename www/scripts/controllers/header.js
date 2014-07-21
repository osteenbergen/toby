define([
    './controllers'
    ],
    function(controllers){
        controllers.controller('HeaderCtrl',[
            '$scope',
            'Status',
            function($scope,Status){
                $scope.isCollapsed=true;
                //Two small functions to check the status
                // otherwise the icons are always visible
                $scope.has_torrent = function(){
                    return Status.get_torrent();
                };
                $scope.has_stream = function(){
                    return Status.get_stream();
                };
            }
        ]);
    }
);
