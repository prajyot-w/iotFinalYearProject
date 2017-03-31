/**
 * Created by prajyot on 30/3/17.
 */

var app = angular.module('home',['ngCookies']);

app.controller("MainCtrl", ["$scope", "$cookies", "$cookieStore", function($scope, $cookies, $cookieStore){
    $scope.loggedIn = true;

    // if($cookieStore.get("username") != undefined && $cookieStore.get("username") != ""
    // && $cookies.get("key") != undefined && $cookies.get("key") != ""){
    //     console.log("Cookies Exists");
    //     // TODO :
    //     // check creds if matching with
    //     // session values and then set
    //     // loggedIn to true
    //     $scope.loggedIn = true;
    // }else{
    //     console.log("Cookies does not exists.");
    //     $scope.loggedIn = false;
    // }

    $scope.logout = function(){
        window.location = '/logout';
    }
}]);