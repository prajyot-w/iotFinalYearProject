var app = angular.module("index",["ngCookies"]);

app.controller("MainCtrl", ["$scope", "$cookies", "$http", function($scope, $cookies, $http){
    $scope.notLoggedIn = false;
    if($cookies.get("username") == undefined && $cookies.get("username") != "" && $cookies.get("key") == undefined && $cookies.get("key") != "" )
     {
         $scope.notLoggedIn = true;
     }else{
        $http.get("/checkcreds").then(function(resp){
            if(resp.data["status"] == "success"){
                window.location="home.html";
            }else{
                $scope.notLoggedIn = true;
            }
        });
     }
}]);