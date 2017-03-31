/**
 * Created by prajyot on 30/3/17.
 */

var app = angular.module('home',['ngCookies']);

app.controller("MainCtrl", ["$scope", "$cookies", "$cookieStore", "MainService", function($scope, $cookies, $cookieStore, MainService){
    $scope.loggedIn = false;

    if($cookieStore.get("username") != undefined && $cookieStore.get("username") != ""
    && $cookies.get("key") != undefined && $cookies.get("key") != ""){
        // TODO :
        // check creds if matching with
        // session values and then set
        // loggedIn to true
        MainService.checkCreds().then(function(resp){
            if(resp.data["status"] == "success"){
                $scope.loggedIn = true;
                MainService.getvehicle().then(function(resp){
                    $scope.vehicleInfo = resp.data;
                });
            }else{
                $scope.loggedIn = false;
                window.location = "/";
            }
        });
    }else{
        $scope.loggedIn = false;
        window.location = "/";
    }

    $scope.logout = function(){
        window.location = '/logout';
    }
}]);

app.service("MainService",["$http", function($http){

    this.getvehicle = function(){
        return $http({
            method: "GET",
            url: "/api/getvehicle"
        });
    };

    this.checkCreds = function(){
        return $http({
            method: "GET",
            url: "/checkcreds"
        });
    };
}]);