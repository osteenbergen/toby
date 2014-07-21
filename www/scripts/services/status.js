define([
    './services'
    ],
    //A small service that is used as a global storage
    function(services){
        services.factory('Status',
            [
                function Status(){
                    var torrent = null;
                    var stream = null;
                    return {
                        get_torrent: function(){
                            return torrent;
                        },
                        set_torrent: function(bool){
                            torrent = bool;
                        },
                        get_stream: function(){
                            return stream;
                        },
                        set_stream: function(bool){
                            stream = bool;
                        }
                    }
                }
            ]
        );
    }
);
