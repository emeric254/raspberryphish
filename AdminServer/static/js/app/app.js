var app = angular.module('MyApp', ['ngMaterial', 'ngMessages']);

app.controller('AppCtrl', function($scope, $http, $mdDialog) {
    $scope.help = function() {
        $mdDialog.show(
            $mdDialog.alert()
                .clickOutsideToClose(true)
                .parent('body')
                .title('Help')
                .textContent('Yayy ~~~ !')
                .ok('Ok')
        );
      originatorEv = null;
    };

//    $scope.ws = new WebSocket('ws://127.0.0.1:4433/ws/');
//    $scope.ws.binaryType = 'arraybuffer';
//
//    $scope.ws.onopen = function() {
//        console.log('Connected.')
//    };
//
//    $scope.ws.onmessage = function(evt) {
//        $scope.$apply(function () {
//            message = JSON.parse(evt.data);
//            $scope.currentPage = parseInt(message['page_no']);
//            $scope.totalRows = parseInt(message['total_number']);
//            $scope.rows = message['data'];
//        });
//    };
//
//    $scope.ws.onclose = function() {
//        console.log('Connection is closed...');
//    };

});
