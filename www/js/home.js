/**
 * Created by prajyot on 30/3/17.
 */

var app = angular.module('home',['ngCookies']);

app.controller("MainCtrl", ["$scope", "$cookies", "$cookieStore", "MainService", function($scope, $cookies, $cookieStore, MainService){
    $scope.loggedIn = false;
    $scope.notificationData = undefined;

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
    };

    $scope.getAllNotifications = function(){
        MainService.getAllNotifications().then(function(resp){
            if(resp.status == 200 && resp.data.status == "success"){
                $scope.notificationData = resp.data.data;
                console.log(resp.data.data);
            }
        });
    };

    $scope.getAllNotifications();
}]);

app.service("MainService",["$http", function($http){

    this.getAllNotifications = function(){
        return $http({
            method: "GET",
            url: "/getallnotifications"
        });
    }

    this.getvehicle = function(){
        return $http({
            method: "GET",
            url: "/getvehicle"
        });
    };

    this.checkCreds = function(){
        return $http({
            method: "GET",
            url: "/checkcreds"
        });
    };
}]);