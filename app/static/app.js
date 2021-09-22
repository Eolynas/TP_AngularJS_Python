// Create an Application named "myApp".
var app = angular.module("ticketApp", []);

// Create a Controller named "myCtrl"
angular.module('ticketApp', [])
    .controller('myCtrl', ['$scope', '$http', function ($scope, $http) {
        $scope.orderByField = 'date_intervention';
        $scope.reverseSort = false;

        $scope.list_interventions = []
        $http.get('/interventions')
            .then(function (response) {
                for (index in response.data) {
                    intervention = status_intervention(response.data[index])
                    response.data[index] = intervention
                    response.data[index].index = parseInt(index) + 1
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
            $http.post("/interventions", JSON.stringify(intervention))
                .then(function (response) {
                    // $scope.books = response.data;
                    // new_inter = status_intervention(intervention)
                    new_inter = status_intervention(response.data)
                    new_inter.index = $scope.list_interventions.length + 1
                    $scope.list_interventions.push(new_inter);
                });

        }

        $scope.deleteIntervention = function (index, intervention_id) {
            var index = index
            $http.delete("/interventions/" + intervention_id)
                .then(function (response) {
                    $scope.list_interventions.splice(index, 1);
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
                // date_intervention: moment(date_intervention).format('DD/MM/YYYY h:mm:ss')
            };
            var index_intervention = index
            $http.put("/interventions/" + intervention_id, JSON.stringify(intervention))
                .then(function (response) {
                    if (moment(response.data.date_intervention) < moment()) {
                        intervention.status = 'Terminé'
                    } else {
                        intervention.status = 'Validé'
                    }

                    for (const [key, value] of Object.entries(intervention)) {
                        if (value === '' || value == null) {
                            intervention.status = 'Brouillon'
                        }
                    }
                    $scope.list_interventions[index] = intervention
                });
        }
    }
    ])
    .config(function ($interpolateProvider) {
        $interpolateProvider.startSymbol('[[').endSymbol(']]');
    });

function status_intervention(data) {
    var status_intervention = 'Validée'
    for (const [key, value] of Object.entries(data)) {
        if (value === '' || value == null) {
            status_intervention = 'Brouillon'
        }
        if (key === 'date_intervention') {
            if (moment(value) < moment()) {
                status_intervention = 'Terminé'
            }
            if (value) {
                data.date_intervention = moment(value).format('DD/MM/YYYY h:mm:ss')
            }
        }
    }
    data.status = status_intervention
    return data
}

$('#modalFormIntervention').on('shown.bs.modal', function () {
    $('#myInput').trigger('focus')
})

// Function for clean modal form
$(document).ready(function () {
    $('#buttonModal').click(function () {
        $("#AddLabelIntervention").val("");
        $("#AddLabelDescription").val("");
        $("#AddLabelAuthor").val("");
        $("#AddLabelLocation").val("");
        $("#AddLabelDate").val("");
    });
});
