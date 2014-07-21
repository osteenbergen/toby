//https://startersquad.com/blog/angularjs-requirejs/
//Clear cache for development
localStorage.clear();
less = {env:'development'};

//Use RequireJS to load all dependencies
require.config({
    paths: {
        domReady : "../bower_components/requirejs-domready/domReady",
        angular : "../bower_components/angular/angular",
        angular_route :"../bower_components/angular-route/angular-route",
        angular_resource :"../bower_components/angular-resource/angular-resource",
        angular_bootstrap_tpls :"../bower_components/angular-bootstrap/ui-bootstrap-tpls",
        angular_fontawesome : "../bower_components/angular-fontawesome/dist/angular-fontawesome",
        angular_match_media : "../bower_components/angular-match-media/angular-match-media",
        less : "../bower_components/less/dist/less-1.7.3"
    },
    //Not all dependencies have AMD support, use shim to wrap the module according to AMD
    shim : {
        angular: {
            exports: "angular"
        },
        angular_route: {
            deps: ['angular'],
            exports: "angular_route"
        },
        angular_resource: {
            deps: ['angular'],
            exports: "angular_resource"
        },
        angular_bootstrap_tpls: {
            deps: ['angular'],
            exports: "angular_bootstrap_tpls"
        },
        angular_fontawesome: {
            deps: ['angular'],
            exports: "angular_fontawesome"
        },
        angular_match_media: {
            deps: ['angular'],
            exports: "angular_match_media"
        },
        less: {
            exports: "less"
        }
    },
    //Use the bootstrap file to load the rest
    deps : ["./bootstrap"]
});

