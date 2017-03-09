(function(){
	var app = angular.module('myApp',['smart-table']);
	
	app.directive("tableForm", function(){
		return{
			restrict: 'E',
			templateUrl: "table-form.html"
		};
	});
	
	app.controller('dataController', function($scope){
		$scope.tableRows = [
			{"professor": "Augenblick", "rating": 4.8, "tags": "Helpful, Friendly", "course": "CS275", "crn": 12356},
			{"professor": "Augenblick", "rating": 4.8, "tags": "Helpful, Friendly", "course": "CS265", "crn": 15366},
			{"professor": "Katsinis", "rating": 3.8, "tags": "Intelligent, Challenging, Cool, Greek ,Friendly", "course": "CS281", "crn": 19856},
			{"professor": "Katsinis", "rating": 3.8, "tags": "Intelligent, Challenging, Cool, Greek ,Friendly", "course": "CS283", "crn": 26862},
			{"professor": "Jodie", "rating": 4.9, "tags": "Easy, Nice, Cool ", "course": "BUSN103", "crn": 98561},
			{"professor": "Jodie", "rating": 4.9, "tags": "Easy, Nice, Cool ", "course": "BUSN102", "crn": 85988},
			{"professor": "Liechty", "rating": 4.2, "tags": "Easy, Dry,  Boring ", "course": "STAT201", "crn": 65844},
			{"professor": "Liechty", "rating": 4.2, "tags": "Easy, Dry,  Boring ", "course": "STAT202", "crn": 65844},
			{"professor": "Liechty", "rating": 4.2, "tags": "Easy, Dry,  Boring ", "course": "STAT201", "crn": 65844},
			{"professor": "Schmidt", "rating": 3.4, "tags": "Structured, Strict", "course": "CS265", "crn": 95722},
			{"professor": "Schmidt", "rating": 3.4, "tags": "Structured, Strict,  ", "course": "CS265", "crn": 95722},
			
			

			
		];
		
		$scope.itemsPerPage = 5;
		
		$scope.newRow = {firstname: "", lastname: "", birthday: '', eyeColor: "", hairColor: ""};
			
		$scope.rowSubmit = function(fname,lname,bday,ecolor,hcolor){
		
			 var clearForm = angular.copy(clearForm);			
			
			$scope.newRow = {firstname: fname, lastname: lname, birthday: new Date(bday) , eyeColor: ecolor, hairColor: hcolor}
			$scope.tableRows.push($scope.newRow);
			$scope.newRow = angular.copy(clearForm);
			$scope.newRow = {firstname: "", lastname: "", birthday: '' , eyeColor: "", hairColor: ""};
		};
		
		$scope.removeRow = function removeRow(row) {
			var index = $scope.tableRows.indexOf(row);
			if (index > -1) {
				$scope.tableRows.splice(index, 1);
			}
		};
		
		});
	
	
})();