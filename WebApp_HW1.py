# Import javascript modules
from js import THREE, window, document, Object,console
#from THREE import MeshLine

#from THREE.MeshLine import MeshLine

# Import pyscript / pyodide modules
from pyodide.ffi import create_proxy, to_js
# Import python module
import math, random


#-----------------------------------------------------------------------
# USE THIS FUNCTION TO WRITE THE MAIN PROGRAM
def main():
    #-----------------------------------------------------------------------
    # VISUAL SETUP
    # Declare the variables
    global renderer, scene, camera, controls,composer, axesHelper, Saved_State
    Saved_State =[]
    
    #Set up the renderer
    renderer = THREE.WebGLRenderer.new()
    renderer.setPixelRatio( window.devicePixelRatio )
    renderer.setSize(window.innerWidth, window.innerHeight)
    document.body.appendChild(renderer.domElement)

 
    
    # Set up the scene
    scene = THREE.Scene.new()
    back_color = THREE.Color.new(0.1,0.1,0.1)
    scene.background = back_color
    camera = THREE.PerspectiveCamera.new(45, window.innerWidth/window.innerHeight, 0.1,9999)
    camera.position.z = 10
    camera.position.y = 10
    camera.position.x = 10

    #pointLight = THREE.PointLight.new( 0xffffff, 1 )
    #camera.add( pointLight )
    #pointLight.position.set( 50, 50, 50 )
    #scene.add(pointLight)
    scene.add(camera)

    # Graphic Post Processing
    global composer
    post_process()

    #axesHelper
    axesHelper = THREE.AxesHelper.new(100)
    scene.add(axesHelper)
    
    # Set up responsive window
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy) 
    #-----------------------------------------------------------------------
    # YOUR DESIGN / GEOMETRY GENERATION
    # Geometry Creation
    global geom1_params, cubes, cube_lines
    
    cubes = []
    cube_lines = []
    geom1_params = {
        "size" : 10,
        "x" : 1, 
        "y" : 1,
        "z" : 1,
        "Scalex" : 1, 
        "Scaley" : 1,
        "Scalez" : 1,
        "rotationx":0,
        "rotationy":0,   
        "rotationz":0,
        "Shear":0,
        "Swell":0,
        "OriginPoint":False,
        "Randomize": Random,
        "Save": Save,
        "Load": Load,
    }
    
    geom1_params = Object.fromEntries(to_js(geom1_params))
    
    #create Materials
    global material, line_material
    
    color = THREE.Color.new(1, 1, 1)
    material = THREE.MeshBasicMaterial.new(color)
    material.transparent = True
    material.opacity = 0.9
    material.color = color
    
    line_material = THREE.LineBasicMaterial.new(color)
    line_material.color = THREE.Color.new(255,0,0)
    
    

    #-----------------------------------------------------------------------
    # USER INTERFACE
    # Set up Mouse orbit control
    controls = THREE.OrbitControls.new(camera, renderer.domElement)

    # Set up GUI
    gui = window.lil.GUI.new()
    param_folder = gui.addFolder('Parameters')
    #param_folder.add(geom1_params, 'size', 10,100,1)
    param_folder.add(geom1_params, 'x', 1,10,1)
    param_folder.add(geom1_params, 'y', 1,10,1)
    param_folder.add(geom1_params, 'z', 1,10,1)
    param_folder.add(geom1_params, 'Scalex', 1,5,0.1)
    param_folder.add(geom1_params, 'Scaley', 1,5,0.1)
    param_folder.add(geom1_params, 'Scalez', 1,5,0.1)
    param_folder.add(geom1_params, 'rotationx', -360,360)
    param_folder.add(geom1_params, 'rotationy', -360,360)
    param_folder.add(geom1_params, 'rotationz', -360,360)
    param_folder.add(geom1_params, 'Shear', 0,2,0.01)
    param_folder.add(geom1_params, 'Swell', 0,50, 0.1)
    param_folder.add(geom1_params, 'OriginPoint', True,False)
    param_folder.add(geom1_params, 'Randomize' )
    param_folder.add(geom1_params, 'Save' )
    param_folder.add(geom1_params, 'Load' )
    
   #param_folder.resetAnimation = Random() {
    
    param_folder.open()
    
    #-----------------------------------------------------------------------
     #generate the boxes using the loop
    Matrix()
    # RENDER + UPDATE THE SCENE AND GEOMETRIES
    render()
    
#-----------------------------------------------------------------------
# HELPER FUNCTIONS
# Updtae tht cubes

def Matrix():
        global cubes

       
        for i in range(geom1_params.x):
           
            for j in range(geom1_params.y):
                
                for k in range(geom1_params.z):
                    
                    if i == 0:
                        ii= geom1_params.Scalex
                        
                    if j == 0:
                        jj= geom1_params.Scaley
                       
                    if k == 0:
                        kk= geom1_params.Scalez
                    
                    if geom1_params.OriginPoint == True:
                        OriginFactor=0
                    else:
                        OriginFactor = 1
                    global BOOL, BOOL2
                    BOOL = geom1_params.OriginPoint
                    BOOL2 = geom1_params.Randomize
                       
                    

                    geom = THREE.BoxGeometry.new(geom1_params.Scalex*1*(geom1_params.Swell*i*j*k*0.01)+ii, geom1_params.Scaley*1*(geom1_params.Swell*i*j*k*0.01)+jj, geom1_params.Scalez*1*(geom1_params.Swell*i*j*k*0.01)+kk)
                    geom.translate(i*(geom1_params.Scalex)*(ii+i*geom1_params.Shear)*OriginFactor, j*(geom1_params.Scaley)*(jj+j*geom1_params.Shear)*OriginFactor, k*(geom1_params.Scalez)*(kk+k*geom1_params.Shear)*OriginFactor)
                    global StopSwell,StopShear,StopRotationX,StopRotationY,StopRotationZ,StopScaleX,StopScaleY,StopScaleZ
                    StopSwell=geom1_params.Swell
                    StopShear=geom1_params.Shear
                    StopRotationX=geom1_params.rotationx
                    StopRotationY=geom1_params.rotationy
                    StopRotationZ=geom1_params.rotationz
                    StopScaleX=geom1_params.Scalex
                    StopScaleY=geom1_params.Scaley
                    StopScaleZ=geom1_params.Scalez
                    

                    geom.rotateX(math.radians(geom1_params.rotationx)/geom1_params.x*i)
                    geom.rotateY(math.radians(geom1_params.rotationy)/geom1_params.y*j)
                    geom.rotateZ(math.radians(geom1_params.rotationz)/geom1_params.z*k)


                
                    cube = THREE.Mesh.new(geom, material)
                    #cube2 = THREE.Mesh.new(geom, material)
                    #cube.rotateY(math.radians(180))
                    
                    cubes.append(cube)
                    #cubes.append(cube2)
                    scene.add(cube) 
                
                    # cubes x
                    
                    

                    edges = THREE.EdgesGeometry.new(cube.geometry)
                    line = THREE.LineSegments.new(edges, line_material)
                    #line2 = THREE.LineSegments.new(edges, line_material)
                    #line.rotateY(math.radians(180))
                    
                    
                    cube_lines.append(line)
                    #cube_lines.append(line2)
                    
                    
                    scene.add(line)
                
                
                    
                    
def Random():
	

    geom1_params.Scalex = random.randint(1,5)
    geom1_params.Scaley = random.randint(1,5)
    geom1_params.Scalez = random.randint(1,5)
    geom1_params.x = random.randint(1,10)
    geom1_params.y = random.randint(1,10)
    geom1_params.z = random.randint(1,10)
    geom1_params.rotationx = random.randint(-360,360)
    geom1_params.rotationy = random.randint(-360,360)
    geom1_params.rotationz = random.randint(-360,360)
    geom1_params.Shear = random.random(0,2,0.01)
    geom1_params.Swell =random.random(0,50, 0.1)

    
    for cube in cubes: scene.remove(cube)
    for cube in cube_lines: scene.remove(cube)
    cubes = []
    cube_lines = []

    
    Matrix()
def Save():
     

    global Saved_State, cubes, cube_lines
    Saved_State =[]

    for cube in cubes: Saved_State.append(cube)
    for cube in cube_lines: Saved_State.append(cube)

   
def Load():
    global Saved_State, cubes, cube_lines

    for cube in cubes: scene.remove(cube)
    for cube in cube_lines: scene.remove(cube)
    
    for cube in Saved_State: scene.add(cube)


    


    
    
    

                          
                    
def update_cubes():
    
    global cubes, cube_lines, material, line_material,Saved_State
    
    # Make sure you dont have zero cubes 
    
    if len(cubes) != 0:
        
        #print(geom1_params.x +geom1_params.y +geom1_params.z)
        #print((len(cubes)+1),(geom1_params.x * geom1_params.y * geom1_params.z)+1)
        
        if len(cubes) != (geom1_params.x * geom1_params.y * geom1_params.z) or StopSwell!= geom1_params.Swell or StopShear!=geom1_params.Shear or StopRotationX!=geom1_params.rotationx or StopRotationY!=geom1_params.rotationy or StopRotationZ!=geom1_params.rotationz or StopScaleX!=geom1_params.Scalex or StopScaleY!=geom1_params.Scaley or StopScaleZ!=geom1_params.Scalez and geom1_params.Randomize== False :
            
            for cube in Saved_State: scene.remove(cube)


            for cube in cubes: scene.remove(cube)
            for cube in cube_lines: scene.remove(cube)
            
            
            cubes = []
            cube_lines = []
            Matrix()
            
            
        if BOOL != geom1_params.OriginPoint and geom1_params.Randomize== False:
            for cube in cubes: scene.remove(cube)
            for cube in cube_lines: scene.remove(cube)
            cubes = []
            cube_lines = []
            Matrix()
        if geom1_params.Randomize== True:
            Random()


        
        

            
        

                
# Simple render and animate
def render(*args):
    window.requestAnimationFrame(create_proxy(render))
    update_cubes()
    controls.update()
    composer.render()

# Graphical post-processing
def post_process():
    render_pass = THREE.RenderPass.new(scene, camera)
    render_pass.clearColor = THREE.Color.new(0,0,0)
    render_pass.ClearAlpha = 0
    fxaa_pass = THREE.ShaderPass.new(THREE.FXAAShader)

    pixelRatio = window.devicePixelRatio

    fxaa_pass.material.uniforms.resolution.value.x = 1 / ( window.innerWidth * pixelRatio )
    fxaa_pass.material.uniforms.resolution.value.y = 1 / ( window.innerHeight * pixelRatio )
   
    global composer
    composer = THREE.EffectComposer.new(renderer)
    composer.addPass(render_pass)
    composer.addPass(fxaa_pass)

# Adjust display when window size changes
def on_window_resize(event):

    event.preventDefault()

    global renderer
    global camera
    
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()

    renderer.setSize( window.innerWidth, window.innerHeight )

    #post processing after resize
    post_process()
#-----------------------------------------------------------------------
#RUN THE MAIN PROGRAM
if __name__=='__main__':
    main()
   