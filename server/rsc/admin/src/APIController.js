(
    function()
    {
        angular
           .module('users')
           .controller('APIController', [ '$scope', '$http', APIController ]);

        function APIController($scope, $http)
        {
            var self = this;

	        self.loadchartlabels = ["CPU", "RAM", "Network", "Disk", "Temp"];
	        self.loadchartseries = ['Current'];
	        self.loadchartdata = [
	            [0, 0, 0, 0, 0]
	        ];

	        self.peerchartlabels = ["Reachable", "Stale", "Delay", "Incomplete"];
	        self.peerchartseries = ['Current'];
	        self.peerchartdata = [
	            [0, 0, 0, 0]
	        ];

	        getSystemLoad();

            function getSystemLoad()
            {
                $http.get("API/system/load")
                    .success(function(response)
                        {
                            self.loadchartdata[0][0] = response.CPU;
                            self.loadchartdata[0][1] = response.RAM;
                            self.loadchartdata[0][3] = response.Storage;
                        });
                setTimeout(getSystemLoad, 1000);
            }
        }
    }
)();
