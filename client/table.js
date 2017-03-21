(function(){
	var app = angular.module('myApp',['smart-table']);
	
	app.directive("tmsTable", function(){
		return{
			restrict: 'E',
			templateUrl: "tms-table.html"
		};
	});
	
	app.controller('dataController', function($scope, $http){
		$scope.tableRows = [];
		$scope.dataLoaded = false;
		$http.get('/all', { cache: true}).success(function(dataFromServer) {
			// set tableRows
			$scope.tableRows = dataFromServer;
			// do any preprocesing
			$scope.dataLoaded = true;
		});			
		});
	
	
})();
