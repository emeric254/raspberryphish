(
    function()
    {
       'use strict';

        angular.module('users')
            .service('userService', ['$q', UserService]);

        /**
        * Users DataService
        * Uses embedded, hard-coded data model; acts asynchronously to simulate
        * remote data service call(s).
        *
        * @returns {{loadAll: Function}}
        * @constructor
        */
        function UserService($q){
            var users = [
                {
                    name: 'UserName',
                    avatar: 'svg-1',
                    email: 'user@mail.lol'
                }
            ];

            // Promise-based API
            return {
                loadAllUsers : function()
                {
                    // Simulate async nature of real remote calls
                    return $q.when(users);
                }
            };
        }

    }
)();
