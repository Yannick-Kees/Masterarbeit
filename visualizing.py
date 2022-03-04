from pointclouds import *


#############################
# 2D point cloud ############
#############################


def draw_phase_field(f,x_,y_, i, film):
    # Creating Contour plot of f
    
    # Parameters:
    #   f:      Function to plot
    #   x_,y_:  Drawing the function on [0,x_] \times [0,y_]

    xlist = np.linspace(-x_, x_, 100)
    ylist = np.linspace(-y_, y_, 100)
    X, Y = np.meshgrid(xlist, ylist)

    Z = [[ f(Tensor([ X[i][j], Y[i][j] ] )).detach().numpy()[0]  for j in range(len(X[0]))  ] for i in range(len(X)) ] # Evaluate function in points
    
    fig = plt.figure()                                                    # Draw contour plot
    levels = [-1000.0,-5.0,-.5,0.0,.5,200.0]                        # Specify contours/level set to plot
    contour = plt.contour(X, Y, Z, levels, colors='k')
    plt.clabel(contour, colors = 'k', fmt = '%2.1f', fontsize=12)
    if film:
        plt.savefig("images/mov/pf" + str(i).zfill(5) + '.jpg')
        plt.close(fig)
    else:
        plt.show()
    return
    
def color_plot(f, y, film):
    # Creating 3D plot of f on [0,1]^2
        
    # Parameters:
    #   f:      Function to plot
    
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    # Make data.
    X = np.arange(-.5, .5, 0.01)
    Y = np.arange(-.5, .5, 0.01)
    X, Y = np.meshgrid(X, Y)
    Z = np.zeros((len(X),len(X[0])))

    for i in range(len(X)):
        for j in range(len(X[0])):
            Z[i][j]= f(Tensor([ X[i][j], Y[i][j] ] )).detach().numpy()[0]

    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)

    # Customize the z axis.
    ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    # ax.zaxis.set_major_formatter('{x:.02f}') # <- This may or may not be out commented, depending on compiler

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)
    if film:
        plt.savefig('images/mov/cp' + str(y).zfill(5) + '.jpg')
        plt.close(fig)
    else:
        plt.show()
    return

#############################
# 2/3D point cloud ##########
#############################



def draw_point_cloud(pc):
    # Plotting point cloud
    
    # Parameters:
    #   pc:      Tensor of points

    d = pc.shape[1] # dimension
    
    if (d==2):
        pointcloud = pc.detach().numpy().T 
        plt.plot(pointcloud[0],pointcloud[1], '.')
        plt.xlim(-.5,.5)
        plt.ylim(-.5,.5)
        plt.show()
        return
    if (d==3):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        pointcloud = pc.detach().numpy().T 
        ax.scatter(pointcloud[0],pointcloud[1],pointcloud[2])
        plt.show()

        
        
#############################
# 3D point cloud ############
#############################       

def plot_implicit(fn, shift=True):
    # Creating 3D contour plot of f on [0,1]^2 using marching cubes 
        
    # Parameters:
    #   fn:      Function to plot
    if shift:
        xa = ya = za= -.5
        xb = yb = zb = .5
    else:
        xa = ya = za= 0.0
        xb = yb = zb = 1.0
    """
    xa = -0.4
    xb = .1
    ya = -.1
    yb  = 0.4
    za = -.4
    zb = .1
    """
    plot = k3d.plot()
    x = np.linspace(xa, xb, 60, dtype=np.float32)
    y = np.linspace(ya, yb, 60, dtype=np.float32)
    z = np.linspace(za,zb, 60, dtype=np.float32)
    x, y, z = np.meshgrid(x, y, z, indexing='ij')
    Z = [[[ fn(Tensor([ x[i][j][k], y[i][j][k], z[i][j][k] ] )).detach().numpy()  for k in range(len(x[0][0]))  ] for j in range(len(x[0])) ] for i in range(len(x)) ]# Evaluate function in points
    plt_iso = k3d.marching_cubes(Z, compression_level=5, xmin=xa, xmax=xb,ymin=ya, ymax=yb,  zmin=za, zmax=zb, level=0.0, flat_shading=False)
    plot += plt_iso
    #plot += plt_iso
    plot.display()



def test_f(t):
    # test function for implicit plotting
    return t[0]**2+t[1]**2+t[2]**2 -1 

