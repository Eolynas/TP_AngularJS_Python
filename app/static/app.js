// Create an Application named "myApp".
var app = angular.module("ticketApp", []);

// Create a Controller named "myCtrl"
angular.module('ticketApp', [])
    .controller('myCtrl', ['$scope', '$http', function ($scope, $http) {
        $scope.message = "Howdy !!";

        $scope.list_interventions = []
        $http.get('/interventions')
            .then(function (response) {
                for (index in response.data) {
                    intervention = status_intervention(response.data[index])
                    response.data[index] = intervention
                }

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
                    new_inter = status_intervention(intervention)
                    $scope.list_interventions.push(new_inter);
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

function status_intervention(data) {
    var status_intervention = 'Validée'
    for (const [key, value] of Object.entries(data)) {
        console.log(`${key}: ${value}`);
        if (value === '' || value == null) {
            status_intervention = 'Brouillon'
        }
        if (key === 'date_intervention') {
            if (moment(value) < moment()) {
                status_intervention = 'Terminé'
            }
        }
    }
    data.status = status_intervention
    return data
}

$('#modalFormIntervention').on('shown.bs.modal', function () {
    $('#myInput').trigger('focus')
})