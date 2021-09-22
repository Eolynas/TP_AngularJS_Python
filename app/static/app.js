// Create an Application named "myApp".
var app = angular.module("ticketApp", []);

// Create a Controller named "myCtrl"
angular.module('ticketApp', [])
    .controller('myCtrl', ['$scope', '$http', function ($scope, $http) {
        $scope.orderByField = 'date_intervention';
        $scope.reverseSort = false;
        // TODO: Ajout d'un message d'erreur (message retour de l'API)
        $scope.message = false;

        $scope.list_interventions = []
        $http.get('/interventions')
            .then(function (response) {
                for (index in response.data) {
                    response.data[index] = response.data[index]
                    response.data[index].index = parseInt(index) + 1
                }
                $scope.list_interventions = response.data
                $scope.message = false
            }, function (response) {
                    $scope.message = response.data
                });
        // TODO: Request post pour ajouter des interventions
        //  Un petit bug arrive si on ajoute des interventions à la suite
        //  Si on met par exemple une description pour la 1er mais pas dans la 2eme, la description de la 1er se met dans la 2eme
        //  Surement à cause du "reset" de ng-model
        $scope.postdata = function (label, description, author, location, date_intervention) {
            var intervention = {
                label: label,
                description: description,
                author: author,
                location: location,
                // TODO: Petite difficulté sur les dates, qui sont sensible à la case
                //  (notamment à cause de SQLlite qui ne prend pas n'importe qu'elle type de format)
                date_intervention: date_intervention
            };
            $http.post("/interventions", JSON.stringify(intervention))
                .then(function (response) {
                    response.data.index = $scope.list_interventions.length + 1
                    $scope.list_interventions.push(response.data);
                    $scope.message = false
                }, function (response) {
                    $scope.message = response.data
                });
        }

        // TODO: Request delete pour supprimer des interventions
        //  Un petit bug arrive si on supprime trop d'intervention d'un coup (visiblement réglé voir README)
        $scope.deleteIntervention = function (index, intervention_id) {
            var index = index
            $http.delete("/interventions/" + intervention_id)
                .then(function (response) {
                    $scope.list_interventions.splice(index, 1);
                    $scope.message = false
                }, function (response) {
                    $scope.message = response.data
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
                    intervention.index = index +1
                    $scope.list_interventions[index] = intervention
                    $scope.message = false
                }, function (response) {
                    $scope.message = response.data
                });
        }
    }
    ])
    .config(function ($interpolateProvider) {
        $interpolateProvider.startSymbol('[[').endSymbol(']]');
    });

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
