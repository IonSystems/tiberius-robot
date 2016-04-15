/*
Template Name: Color Admin - Responsive Admin Dashboard Template build with Twitter Bootstrap 3.3.5
Version: 1.9.0
Author: Sean Ngu
Website: http://www.seantheme.com/color-admin-v1.9/admin/
*/

var handleJstreeDefault = function() {
    $('#jstree-waypoints').jstree({
        "core": {
            "check_callback": true,
            "themes": {
                "responsive": false
            }
        },
        "types": {
            "default": {
                "icon": "fa fa-map text-warning fa-lg"
            },
            "task": {
                "icon": "fa fa-tasks text-warning fa-lg"
            },
            "waypoint": {
                "icon": "fa fa-map-marker text-warning fa-lg"
            }
        },
        "plugins": ["types"]
    });

    $('#jstree-waypoints').on('select_node.jstree', function(e,data) {
        var link = $('#' + data.selected).find('a');
        if (link.attr("href") != "#" && link.attr("href") != "javascript:;" && link.attr("href") != "") {
            if (link.attr("target") == "_blank") {
                link.attr("href").target = "_blank";
            }
            document.location.href = link.attr("href");
            return false;
        }
    });
};


var TreeView = function () {
	"use strict";
    return {
        //main function
        init: function () {
            handleJstreeDefault();
        }
    };
}();
