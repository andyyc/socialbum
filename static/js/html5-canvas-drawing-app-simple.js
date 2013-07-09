// Copyright 2010 William Malone (www.williammalone.com)
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
var drawingApp = (function(){

    var canvas;
    var context;
//var width = (window.innerWidth > 0) ? window.innerWidth : screen.width;
    var width = 320;
//var height = (window.innerHeight > 0) ? window.innerHeight : screen.height;
    var height = 346;
//var canvasWidth = $('#canvasSimpleToolsDiv').width();
    var canvasWidth = width;
    var canvasHeight = height;
//    var canvasHeight = height+100-40-30-40;
    var padding = 25;
    var lineWidth = 8;
    var colorPurple = "#cb3594";
    var colorGreen = "#659b41";
    var colorYellow = "#ffcf33";
    var colorBrown = "#986928";
    var colorWhite = "#ffffff";
    var clickX = new Array();
    var clickY = new Array();
    var clickColor = new Array();
    var clickSize = new Array();
    var clickDrag = new Array();
    var paint = false;
    var curColor = colorPurple;
    var curTool = "marker";
    var curSize = "normal";
    var clickX_simpleTools = new Array();
    var clickY_simpleTools = new Array();
    var clickDrag_simpleTools = new Array();
    var clickColor_simpleTools = new Array();
    var clickSize_simpleTools = new Array();
    var paint_simpleTools;
    var canvas_simpleTools;
    var context_simpleTools;
    var curColor_simpleTools = colorPurple;
    var curSize_simpleTools = "normal";
    var mouseDown = 0;

    function createCanvas(submission_idx){

        submission_idx = (typeof submission_idx === "undefined") ? 0 : submission_idx;
        // Create the canvas (Neccessary for IE because it doesn't know what a canvas element is)
        //var canvasDiv = document.getElementById('canvasSimpleToolsDiv');
        var canvasDiv = $('.canvasSimpleToolsDiv[name=' + submission_idx + ']')[0];
        canvas_simpleTools = document.createElement('canvas');
        canvas_simpleTools.setAttribute('width', canvasWidth);
        canvas_simpleTools.setAttribute('height', canvasHeight);
        canvas_simpleTools.setAttribute('class', 'canvasSimpleTools');
        canvasDiv.appendChild(canvas_simpleTools);
        if(typeof G_vmlCanvasManager != 'undefined') {
            canvas_simpleTools = G_vmlCanvasManager.initElement(canvas_simpleTools);
        }
        context_simpleTools = canvas_simpleTools.getContext("2d"); // Grab the 2d canvas context
        // Note: The above code is a workaround for IE 8 and lower. Otherwise we could have used:
        //     context = document.getElementById('canvas').getContext("2d");
    }

    var prepareSimpleToolsCanvas = function()
    {
        createCanvas();
        // Add mouse events
        // ----------------
        $('body').mousedown(function(e){ mouseDown=1; });
        $('body').mouseup(function(e){ mouseDown=0; });
        $('body').mouseenter(function(e) { mouseDown=0; });

        var touchPress = function(e){
            e.preventDefault();
            var mouseX = e.originalEvent.touches[0].pageX - this.offsetLeft;
            var mouseY = e.originalEvent.touches[0].pageY - this.offsetTop;
            press(mouseX, mouseY);
        }
        var mousePress = function(e){
            e.preventDefault();
            var mouseX = e.pageX - this.offsetLeft;
            var mouseY = e.pageY - this.offsetTop;
            press(mouseX, mouseY)
        }
        var press = function(mouseX, mouseY){
            // Mouse down location
            paint_simpleTools = true;
            addClickSimpleTools(mouseX, mouseY, false);
            // redrawSimpleTools();
        };
        var touchDrag = function(e){
            e.preventDefault();
            var mouseX = e.originalEvent.touches[0].pageX - this.offsetLeft;
            var mouseY = e.originalEvent.touches[0].pageY - this.offsetTop;
            drag(mouseX, mouseY);
        }
        var mouseDrag = function(e){
            e.preventDefault();
            var mouseX = e.pageX - this.offsetLeft;
            var mouseY = e.pageY - this.offsetTop;
            drag(mouseX, mouseY)
        }
        var drag = function(mouseX, mouseY){
            if(paint_simpleTools){
                addClickSimpleTools(mouseX, mouseY, true);
                // redrawSimpleTools();
            }
        };

        var release = function(e){
            e.preventDefault();
            paint_simpleTools = false;
            // redrawSimpleTools();
        }

        var cancel = function(e){
            e.preventDefault();
            paint_simpleTools = false;
        }

        $('.canvasSimpleToolsDiv').mousedown(mousePress);
        $('.canvasSimpleToolsDiv').mousemove(mouseDrag);
        $('.canvasSimpleToolsDiv').mouseup(release);
        $('.canvasSimpleToolsDiv').mouseleave(cancel);

        $('.canvasSimpleToolsDiv').bind('touchstart', touchPress);
        $('.canvasSimpleToolsDiv').bind('touchmove', touchDrag);
        $('.canvasSimpleToolsDiv').bind('touchend', release);
        $('.canvasSimpleToolsDiv').bind('touchcancel', cancel);

        $('.canvasSimpleToolsDiv').mouseenter(function(e){

            if(mouseDown){
                paint_simpleTools = true;
                addClickSimpleTools(e.pageX - this.offsetLeft, e.pageY - this.offsetTop, false);
                // redrawSimpleTools();
            }
            else{
                paint_simpleTools = false;
            }
        });



        $('#choosePurpleSimpleTools').mousedown(function(e){
            curColor_simpleTools = colorPurple;
        });
        $('#chooseGreenSimpleTools').mousedown(function(e){
            curColor_simpleTools = colorGreen;
        });
        $('#chooseYellowSimpleTools').mousedown(function(e){
            curColor_simpleTools = colorYellow;
        });
        $('#chooseBrownSimpleTools').mousedown(function(e){
            curColor_simpleTools = colorBrown;
        });
        $('#chooseSmallSimpleTools').mousedown(function(e){
            curSize_simpleTools = "small";
        });
        $('#chooseNormalSimpleTools').mousedown(function(e){
            curSize_simpleTools = "normal";
        });
        $('#chooseLargeSimpleTools').mousedown(function(e){
            curSize_simpleTools = "large";
        });
        $('#chooseHugeSimpleTools').mousedown(function(e){
            curSize_simpleTools = "huge";
        });
        $('#chooseEraserSimpleTools').mousedown(function(e){
            curColor_simpleTools = colorWhite;
        });

        $('#clearCanvasSimpleTools').mousedown(function(e)
        {
            clickX_simpleTools = new Array();
            clickY_simpleTools = new Array();
            clickDrag_simpleTools = new Array();
            clickColor_simpleTools = new Array();
            clickSize_simpleTools = new Array();
            clearCanvas_simpleTools();
        });

        $('#draw-form').submit(function(){

            $("#draw-form input:hidden[name='clickX']").val(clickX_simpleTools);
            $("#draw-form input:hidden[name='clickY']").val(clickY_simpleTools);
            $("#draw-form input:hidden[name='clickColor']").val(clickColor_simpleTools);
            $("#draw-form input:hidden[name='clickSize']").val(clickSize_simpleTools);
            $("#draw-form input:hidden[name='clickDrag']").val(clickDrag_simpleTools);

            return true;
        });

    }

    function addClickSimpleTools(x, y, dragging)
    {
        clickX_simpleTools.push(x);
        clickY_simpleTools.push(y);
        clickDrag_simpleTools.push(dragging);
        clickColor_simpleTools.push(curColor_simpleTools);
        clickSize_simpleTools.push(curSize_simpleTools);
        addStrokeSimpleTools(x, y, dragging);
    }

    function addStrokeSimpleTools(x, y, dragging)
    {
        var radius;
        var numStrokes = clickDrag_simpleTools.length;
        context_simpleTools.lineJoin = "round";


        if(clickSize_simpleTools[numStrokes-1] == "small"){
            radius = 2;
        }else if(clickSize_simpleTools[numStrokes-1] == "normal"){
            radius = 5;
        }else if(clickSize_simpleTools[numStrokes-1] == "large"){
            radius = 10;
        }else if(clickSize_simpleTools[numStrokes-1] == "huge"){
            radius = 20;
        }

        context_simpleTools.beginPath();
        if(numStrokes > 1 && clickDrag_simpleTools[numStrokes-1]){
            context_simpleTools.moveTo(clickX_simpleTools[numStrokes-2], clickY_simpleTools[numStrokes-2]);
        }
        else{
            context_simpleTools.moveTo(clickX_simpleTools[numStrokes-1]-1, clickY_simpleTools[numStrokes-1]);
        }
        context_simpleTools.lineTo(clickX_simpleTools[numStrokes-1], clickY_simpleTools[numStrokes-1]);
        context_simpleTools.closePath();
        context_simpleTools.strokeStyle = clickColor_simpleTools[numStrokes-1];
        context_simpleTools.lineWidth = radius;
        context_simpleTools.stroke();
    }

    function clearCanvas_simpleTools()
    {
        context_simpleTools.fillStyle = '#ffffff'; // Work around for Chrome
        context_simpleTools.fillRect(0, 0, canvasWidth, canvasHeight); // Fill in the canvas with white
        canvas_simpleTools.width = canvas_simpleTools.width; // clears the canvas
    }

    function redrawSimpleTools()
    {
        clearCanvas_simpleTools();

        var radius;
        context_simpleTools.lineJoin = "round";

        for(var i=0; i < clickX_simpleTools.length; i++)
        {
            if(clickSize_simpleTools[i] == "small"){
                radius = 2;
            }else if(clickSize_simpleTools[i] == "normal"){
                radius = 5;
            }else if(clickSize_simpleTools[i] == "large"){
                radius = 10;
            }else if(clickSize_simpleTools[i] == "huge"){
                radius = 20;
            }

            context_simpleTools.beginPath();
            console.log(clickX_simpleTools[i]);
            console.log(clickY_simpleTools[i]);

            if(clickDrag_simpleTools[i] != 'false' && i){
                console.log("a");
                context_simpleTools.moveTo(clickX_simpleTools[i-1], clickY_simpleTools[i-1]);
            }else{
                console.log("b");
                console.log(parseInt(clickX_simpleTools[i]));
                context_simpleTools.moveTo(parseInt(clickX_simpleTools[i])-1, parseInt(clickY_simpleTools[i]));
            }
            context_simpleTools.lineTo(parseInt(clickX_simpleTools[i]), parseInt(clickY_simpleTools[i]));
            context_simpleTools.closePath();
            context_simpleTools.strokeStyle = clickColor_simpleTools[i];
            context_simpleTools.lineWidth = radius;
            context_simpleTools.stroke();
        }
    }

    var drawImage = function(clickX, clickY, clickColor, clickSize, clickDrag, submission_idx) {
        clickX_simpleTools = clickX.split(",");
        clickY_simpleTools = clickY.split(",");
        clickColor_simpleTools = clickColor.split(",");
        clickSize_simpleTools = clickSize.split(",");
        clickDrag_simpleTools = clickDrag.split(",");
        createCanvas(submission_idx);
        redrawSimpleTools();
    };

    return {
        drawImage : drawImage,
        prepareSimpleToolsCanvas : prepareSimpleToolsCanvas
    }
}());