/**
 * Created by xiaoming on 17/8/17.
 */
$("button").click(function () {
    $.get("/test",function (data, status) {
        alert(data+status);
    });
});

var app = angular.module('myApp', []);
app.controller('myCtrl', function($scope, $http) {
    $http.get("/test").then(function (reponse) {
        $scope.name='success';
    },function (response) {
        $scope.name="fail";
    });
});
app.controller('myCtrl3', function($scope, $http) {
    $http.get("/test").then(function (reponse) {
        $scope.name='success';
    },function (response) {
        $scope.name="fail";
    });
});

var app2 = angular.module('myApp2',[]);
app2.controller('myCtrl2',function($scope){});

angular.element(document).ready(function() {
    angular.bootstrap(document.getElementById('app2'), ['myApp2']);
});
