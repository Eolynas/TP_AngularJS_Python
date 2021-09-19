// Create an Application named "myApp".
var app = angular.module("ticketApp", []);

// Create a Controller named "myCtrl"
angular.module('ticketApp', [])
    .controller('myCtrl', ['$scope', '$http', function ($scope, $http) {
        $scope.message = "Howdy !!";

        $scope.list_interventions = []
        $http.get('/interventions')
            .then(function (response) {
                $scope.list_interventions = response.data
            });
        $scope.postdata = function (label, description, author, location, date_intervention) {
            var intervention = {
                label: label,
                description: description,
                author: author,
                location: location,
                date_intervention: date_intervention
            };
            console.log(intervention)
            $http.post("/intervention/add", JSON.stringify(intervention))
                .then(function (response) {
                    // $scope.books = response.data;
                    $scope.list_interventions.push(intervention);
                });

        }

        $scope.deleteIntervention = function (intervention_id) {
            console.log(intervention_id)
            $http.delete("/intervention/" + intervention_id)
                .then(function (response) {
                    // $scope.books = response.data;
                    $scope.list_interventions.splice($scope.list_interventions.indexOf(intervention_id), 1);
                });

        }

        $scope.editIntervention = function (index, intervention_id, label, description, author, location, date_intervention) {
            var intervention = {
                intervention_id: intervention_id,
                label: label,
                description: description,
                author: author,
                location: location,
                date_intervention: date_intervention
            };
            $http.put("/intervention/" + intervention_id, JSON.stringify(intervention))
                .then(function (response, index) {
                    // $scope.books = response.data;

                });
            $scope.list_interventions[index]['date_intervention'] = intervention['date_intervention']

        }

    }
    ])
    .config(function ($interpolateProvider) {
        $interpolateProvider.startSymbol('[[').endSymbol(']]');
    });


$('#modalFormIntervention').on('shown.bs.modal', function () {
    $('#myInput').trigger('focus')
})