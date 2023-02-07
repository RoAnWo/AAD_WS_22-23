# Import javascript modules
from js import THREE, window, document, Object, console
# Import pyscript / pyodide modules
from pyodide.ffi import create_proxy, to_js
# Import python module
import math
#from random import randint

	
#-----------------------------------------------------------------------
# USE THIS FUNCTION TO WRITE THE MAIN PROGRAM
global geom1_params
geom1_params = {
    "size" : 1,
    
          
    }
geom1_params = Object.fromEntries(to_js(geom1_params))

def main():
    #-----------------------------------------------------------------------
    # VISUAL SETUP
    # Declare the variables
    global renderer, scene, camera, controls,composer
    
    #Set up the renderer
    renderer = THREE.WebGLRenderer.new()
    renderer.setPixelRatio( window.devicePixelRatio )
    renderer.setSize(window.innerWidth, window.innerHeight)
    document.body.appendChild(renderer.domElement)

    # Set up the scene
    scene = THREE.Scene.new()
    back_color = THREE.Color.new(0.1,0.1,0.1)
    scene.background = back_color
    camera = THREE.PerspectiveCamera.new(75, window.innerWidth/window.innerHeight, 0.1, 9999)
    camera.position.z = 500
    scene.add(camera)

    # Graphic Post Processing
    global composer
    post_process()

    # Set up responsive window
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy) 
    #-----------------------------------------------------------------------
    # YOUR DESIGN / GEOMETRY GENERATION
    # Geometry Creation
    
    
    
    
            
    my_axiom_system = system(0, geom1_params.size, "X")
    draw_system((my_axiom_system), THREE.Vector3.new(0,0,0))



    #-----------------------------------------------------------------------
    # USER INTERFACE
    # Set up Mouse orbit control
    controls = THREE.OrbitControls.new(camera, renderer.domElement)

    # Set up GUI
    gui = window.lil.GUI.new()
    param_folder = gui.addFolder('Parameters')
    param_folder.add(geom1_params, 'size', 1,4,1)
    
    param_folder.open()
    
    
    
    #-----------------------------------------------------------------------
    # RENDER + UPDATE THE SCENE AND GEOMETRIES
    render()
    
    
#-----------------------------------------------------------------------
# HELPER FUNCTIONS


#print(Maximum,geom1_params.size)

#### update   
def update():
    global Z
    
            
    if Z is not geom1_params.size:
        for Lines in lineList: 
                scene.remove(Lines)

        my_axiom_system = system(0, geom1_params.size, "X")
        
        draw_system((my_axiom_system), THREE.Vector3.new(0,0,0))
        


# Define RULES in a function which takes one SYMBOL and applies rules generation
def generate(symbol):
    if symbol == "X":
        return "XF[*X][/X][+X][-X]"    
    elif symbol == "F":
        return "FF"
    elif symbol == "+":
        return "+"
    elif symbol == "-":
        return "-"
    elif symbol == "[":
        return "["
    elif symbol == "]":
        return "]"
    #elif symbol == "(":
       #return "("
    #elif symbol == ")":
        #return ")"
    elif symbol == "*":
        return "*"
    elif symbol == "/":
        return "/"


# A recursive fundtion, which taken an AXIOM as an inout and runs the generate function for each symbol
def system(current_iteration, max_iterations, axiom):
        global Z
           
        
    
        current_iteration += 1
        
        
    
        new_axiom = ""
        for symbol in axiom:
            new_axiom += generate(symbol)
        if current_iteration >= max_iterations:
            Z = current_iteration
            return new_axiom
       # if max_iterations >= current_iteration:
            
           # return system(current_iteration, max_iterations, new_axiom)
            
        
        else:
            return system(current_iteration, max_iterations, new_axiom)







def draw_system(axiom, start_pt):
    move_vec = THREE.Vector3.new(0,15,0)
    
    global old_move_vec,old_state, lines, line, vis_line,lineList
    old_states = []
    old_move_vecs = []
    lines = []
    lineList = []
    
    
    
    for symbol in axiom:
        if symbol == "F" or symbol == "X":
            old = THREE.Vector3.new(start_pt.x, start_pt.y, start_pt.z)
            new_pt = THREE.Vector3.new(start_pt.x, start_pt.y, start_pt.z)
            new_pt = new_pt.add(move_vec)
            line = []
            line.append(old)
            line.append(new_pt)
            lines.append(line)
            start_pt = new_pt

            



            

        elif symbol == "+": 
            move_vec.applyAxisAngle(THREE.Vector3.new(0,0,1), math.radians(45) )
        
        elif symbol == "-":
            move_vec.applyAxisAngle(THREE.Vector3.new(0,0,1), -math.radians(45))
       
        elif symbol == "*": 
            move_vec.applyAxisAngle(THREE.Vector3.new(1,0,0), math.radians(45))
        
        elif symbol == "/":
            move_vec.applyAxisAngle(THREE.Vector3.new(1,0,0), -math.radians(45))
        
        
        elif symbol == "[":
            old_state = THREE.Vector3.new(start_pt.x, start_pt.y, start_pt.z)
            old_move_vec = THREE.Vector3.new(move_vec.x, move_vec.y, move_vec.z)
            old_states.append(old_state)
            old_move_vecs.append(old_move_vec)
        

        elif symbol == "]":
            start_pt = THREE.Vector3.new(old_states[-1].x, old_states[-1].y, old_states[-1].z)
            move_vec = THREE.Vector3.new(old_move_vecs[-1].x, old_move_vecs[-1].y, old_move_vecs[-1].z)
            old_states.pop(-1)
            old_move_vecs.pop(-1)
    
    for points in lines:
        points = to_js(points)
        
        line_geom  = THREE.BufferGeometry.new().setFromPoints( points )
        line_geom2 = THREE.BufferGeometry.new().setFromPoints( points )
        line_geom3 = THREE.BufferGeometry.new().setFromPoints( points )
        line_geom4 = THREE.BufferGeometry.new().setFromPoints( points )
        line_geom5 = THREE.BufferGeometry.new().setFromPoints( points )
        line_geom6 = THREE.BufferGeometry.new().setFromPoints( points )

       
        
       
    
        

        
        
        

        material = THREE.LineBasicMaterial.new()
        vis_line = THREE.Line.new( line_geom, material )
        vis_line2 = THREE.Line.new( line_geom2, material )
        vis_line3 = THREE.Line.new( line_geom3, material )
        vis_line4 = THREE.Line.new( line_geom4, material )
        vis_line5 = THREE.Line.new( line_geom5, material )
        vis_line6 = THREE.Line.new( line_geom6, material )
        line_geom2.rotateX(math.radians(180))
        line_geom3.rotateX(math.radians(90))
        line_geom4.rotateX(math.radians(-90))
        line_geom5.rotateZ(math.radians(90))
        line_geom6.rotateZ(math.radians(-90))
        
        
        
    
        
        lineList.append(vis_line)
        lineList.append(vis_line2)
        lineList.append(vis_line3)
        lineList.append(vis_line4)
        lineList.append(vis_line5)
        lineList.append(vis_line6)

        
    
                
        global scene
        scene.add(vis_line,vis_line2, vis_line3,vis_line4,vis_line5,vis_line6)



# Simple render and animate
def render(*args):
    window.requestAnimationFrame(create_proxy(render))
    update()
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