import * as THREE from './build/three.module.js';
import {PointerLockControls} from './control/PointerLockControls.js';
import {EffectComposer} from './extra/EffectComposer.js';
import {ShaderPass} from './extra/ShaderPass.js';
import {OutlinePass} from './extra/OutlinePass.js';
import {RenderPass} from './extra/RenderPass.js';
import {FXAAShader} from './extra/FXAAShader.js';

import {DRACOLoader} from './extra/DRACOLoader.js';


import {OrbitControls} from "https://unpkg.com/three@0.112/examples/jsm/controls/OrbitControls.js";
import {GLTFLoader} from "https://cdn.rawgit.com/mrdoob/three.js/master/examples/jsm/loaders/GLTFLoader.js";

let camera, scene, renderer, controls;

let composer, effectFXAA, outlinePass;

const objects = [];

let raycaster;

let moveForward = false;
let moveBackward = false;
let moveLeft = false;
let moveRight = false;
let canJump = false;

let prevTime = performance.now();
const velocity = new THREE.Vector3();
const direction = new THREE.Vector3();
const vertex = new THREE.Vector3();
const color = new THREE.Color();

var rotate_avail = false;

// tea_take2
let model_path = "/static/model/" + Server.model;

function init() {

    console.log("model init")
    var container = document.createElement('div');

    $(".model-show-wrapper").append(container);

    let width = (window.innerWidth / 3) * 2;
    let height = window.innerHeight;
    renderer = new THREE.WebGLRenderer({
        antialias: false,
        //是否保留缓冲区直到手动清除或覆盖
        preserveDrawingBuffer: true
    });
    renderer.shadowMap.enabled = true;

    width = $("#progress-container").innerWidth();
    height = $("#progress-container").innerHeight();


    renderer.setSize(width, height);

    $("#image-view").css('top', -height + 105);
    // // window.console.log("DSAD", width)
    // renderer.setSize(width, height);

    let cssStyle = `width:${width}px; height:${height}px`;
    renderer.domElement.style = cssStyle;
    renderer.domElement.className = "model-wrapper";
    renderer.domElement.id = "model-wrapper";
    container.append(renderer.domElement);

    scene = new THREE.Scene();

    // scene.background = new THREE.Color('#b9cec3');
    scene.background = new THREE.Color('#cdcbce');
    scene.fog = new THREE.Fog(scene.background, 1, 100);


    camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
    camera.position.set(0, 0, 8);

    controls = new OrbitControls(camera, renderer.domElement);
    controls.minDistance = 5;
    controls.maxDistance = 20;
    controls.enablePan = false;
    controls.enableDamping = true;
    controls.dampingFactor = 0.25;

    function zoomIn() {
        camera.fov = camera.fov + 5;
    }

    function zoomOut() {
        camera.fov = camera.fov - 5;
    }

    function switchRotate() {
        console.log(rotate_avail);
        rotate_avail = !rotate_avail
    }


    scene.add(new THREE.AmbientLight(0xebebeb));

    var light = new THREE.DirectionalLight(0xffffff, 0.7);
    light.position.set(0, 1, 1);

    light.castShadow = true;

    light.shadow.mapSize.width = 1024;
    light.shadow.mapSize.height = 1024;

    var d = 10;

    light.shadow.camera.left = -d;
    light.shadow.camera.right = d;
    light.shadow.camera.top = d;
    light.shadow.camera.bottom = -d;

    light.shadow.camera.far = 1000;

    scene.add(light);


    var light2 = new THREE.DirectionalLight(0xffffff, 0.4);
    light2.position.set(-1, 0.1, 0);

    light2.castShadow = false;

    light2.shadow.mapSize.width = 1024;
    light2.shadow.mapSize.height = 1024;

    var d = 10;

    light2.shadow.camera.left = -d;
    light2.shadow.camera.right = d;
    light2.shadow.camera.top = d;
    light2.shadow.camera.bottom = -d;

    light2.shadow.camera.far = 1000;

    scene.add(light2);

    var light3 = new THREE.DirectionalLight(0xddffdd, 0.2);
    light3.position.set(0.5, -0.2, 0);

    light3.castShadow = false;

    light3.shadow.mapSize.width = 1024;
    light3.shadow.mapSize.height = 1024;

    var d = 10;

    light3.shadow.camera.left = -d;
    light3.shadow.camera.right = d;
    light3.shadow.camera.top = d;
    light3.shadow.camera.bottom = -d;

    light3.shadow.camera.far = 1000;

    scene.add(light3);

    // 加载进度
    var manager = new THREE.LoadingManager();
    manager.onProgress = function (item, loaded, total) {
        console.log(item, loaded, total);
    };

    function sleep(time) {
        return new Promise((resolve) => setTimeout(resolve, time));
    }

    // progress load
    let progress_number = 0;
    var timer = setInterval(function () {
        if (progress_number < progress || progress >= 99) {
            progress_number = Number(progress_number) + 1;
        } else {
        }
        if (progress_number > 105) {
            clearInterval(timer);
            sleep(500).then(() => {
                $(".show-controls").toggleClass("wrapper-hidden");
                $(".show-controls2").toggleClass("wrapper-hidden");
                $(".progress-wrapper").toggleClass("wrapper-hidden");
            })
            return;
        }
        $(".bar").attr("class", "bar white bar-" + String(progress_number));
    }, 50)


    var progress = 0;
    //进度通知
    let onProgress = function (xhr) {
        if (xhr.lengthComputable) {
            let percentComplete = xhr.loaded / xhr.total * 100;
            console.log("progress:", Math.round(percentComplete, 2));
            progress = Math.ceil(percentComplete);
        }
    };

    let mouse = new THREE.Vector2();
    let group = new THREE.Group();
    let obj3d = new THREE.Object3D();
    var loader = new GLTFLoader();

    const loader2 = new GLTFLoader(), path = model_path;

    var dracoLoader = new DRACOLoader();
    dracoLoader.setDecoderPath('../../static/js/threejs/libs/gltf/');
    loader.setDRACOLoader(dracoLoader);
    loader.load(
        path,
        (gltf) => {
            // called when the resource is loaded
            gltf.scene.scale.set(0.5, 0.5, 0.5) // scale here
            scene.add(gltf.scene);
        }, onProgress,
        function (error) {
            console.log('An error happened', error);
        });

    // loader.load(model_path, function (gltf) {
    //         // 输出模型各面
    //         window.console.log(gltf);
    //         // gltf.scene.traverse(function (child) {
    //         //     if (child.isMesh) {
    //         //         child.frustumCulled = false;
    //         //         //模型阴影
    //         //         child.castShadow = true;
    //         //         //模型自发光
    //         //         //child.material.emissive = child.material.color;
    //         //         //child.material.emissiveMap = child.material.map;
    //         //     }
    //         // });
    //         gltf.scene.scale.set(0.5, 0.5, 0.5) // scale here
    //         // obj3d.add(gltf.scene);
    //         obj3d.add(gltf.scene);
    //     }, onProgress,
    //     function (error) {
    //         console.log('An error happened', error);
    //     });


    group.add(obj3d);
    scene.add(group);


    // var floorMaterial = new THREE.MeshLambertMaterial({
    //     color: '#a9a8a8',
    // });
    // var floorGeometry = new THREE.CircleBufferGeometry(7, 50);
    // var floorMesh = new THREE.Mesh(floorGeometry, floorMaterial);
    // floorMesh.rotation.x -= Math.PI * 0.5;
    // floorMesh.position.y -= 1.5;
    // group.add(floorMesh);
    // floorMesh.receiveShadow = true;


    // stats = new Stats();
    // container.appendChild(stats.dom);


    // postprocessing
    composer = new EffectComposer(renderer);

    var renderPass = new RenderPass(scene, camera);
    composer.addPass(renderPass);

    outlinePass = new OutlinePass(new THREE.Vector2(window.innerWidth, window.innerHeight), scene, camera);
    composer.addPass(outlinePass);


    var onLoad = function (texture) {
        outlinePass.patternTexture = texture;
        texture.wrapS = THREE.RepeatWrapping;
        texture.wrapT = THREE.RepeatWrapping;
    };

    effectFXAA = new ShaderPass(FXAAShader);
    effectFXAA.uniforms['resolution'].value.set(1 / window.innerWidth, 1 / window.innerHeight);
    effectFXAA.renderToScreen = true;
    composer.addPass(effectFXAA);


    window.addEventListener('resize', onWindowResize, false);

    window.addEventListener('click', onTouchMove);

    function onTouchMove(event) {
        var x, y;
        if (event.changedTouches) {
            x = event.changedTouches[0].pageX;
            y = event.changedTouches[0].pageY;
        } else {
            x = event.clientX;
            y = event.clientY;
        }
        let mainCanvas = renderer.domElement;
        // mainCanvas 就是 canvas元素（renderer.domElement）
        mouse.x = ((event.clientX - mainCanvas.getBoundingClientRect().left) / mainCanvas.offsetWidth) * 2 - 1;// 标准设备横坐标
        mouse.y = -((event.clientY - mainCanvas.getBoundingClientRect().top) / mainCanvas.offsetHeight) * 2 + 1;// 标准设备纵坐标
        // mouse.x = (x / window.innerWidth) * 2 - 1;
        // mouse.y = -(y / window.innerHeight) * 2 + 1;
        // checkIntersection();
    }


    function onWindowResize() {
        var width = window.innerWidth;
        var height = window.innerHeight;

        camera.aspect = width / height;
        camera.updateProjectionMatrix();

        width = $("#progress-container").innerWidth();
        height = $("#progress-container").innerHeight();


        $("#image-view").css('top', -height + 105);
        // window.console.log("DSAD", width)
        renderer.setSize(width, height);

        // composer.setSize(width * 0.67, height * 0.67);

        // effectFXAA.uniforms['resolution'].value.set(1 / window.innerWidth, 1 / window.innerHeight);
    }


    $(".model-outer-wrapper").on('click', ".switch-rotate", function () {
        switchRotate()
    });

    $(".model-outer-wrapper").on('click', ".model-zoom-in", function () {
        zoomIn()
    });

    $(".model-outer-wrapper").on('click', ".model-zoom-out", function () {
        zoomOut()
    });

    function animate() {
        requestAnimationFrame(animate);
        // stats.begin();
        var timer = performance.now();
        // if (params.rotate) {
        //     group.rotation.y = timer * 0.0001;
        // }
//         let params = {
//     edgeStrength: 3.0,
//     edgeGlow: 0.0,
//     edgeThickness: 1.0,
//     pulsePeriod: 0,
//     rotate: false,
//     usePatternTexture: false
// };
        if (rotate_avail) {
            scene.children[scene.children.length - 1].rotateY(0.001 * 5);//旋转角速度0.001弧度每毫秒
        }
        camera.updateProjectionMatrix();
        controls.update();
        composer.render();
        // stats.end();
    }

    animate();
}

init();