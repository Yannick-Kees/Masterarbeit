from loss_functionals import *

####################
# Settings #########
####################

# Neuronal Network
NUM_TRAINING_SESSIONS = 25000
START_LEARNING_RATE = 0.01
PATIENCE = 1500
NUM_NODES = 128

# Phase-Loss
MONTE_CARLO_SAMPLES = 200
MONTE_CARLO_BALL_SAMPLES = 50
EPSILON = .001
CONSTANT = 50.0
MU = 0.1


####################
# Main #############
####################

network = small_MLP3D(NUM_NODES)
network.to(device) 
optimizer = optim.Adam(network.parameters(), START_LEARNING_RATE )
scheduler = ReduceLROnPlateau(optimizer, 'min', patience=PATIENCE, verbose=False)

file = open("3dObjects/cube.off")    
pc = read_off(file)
cloud = torch.tensor(normalize(pc) )


pointcloud = Variable( cloud , requires_grad=True).to(device)

for i in range(NUM_TRAINING_SESSIONS+1):
    # training the network
    # feed forward
    # Omega = [0,1]^2
    
    loss = Phase_loss(network, pointcloud, EPSILON, MONTE_CARLO_SAMPLES, MONTE_CARLO_BALL_SAMPLES, CONSTANT, MU, 3)
    
    if (i%50==0):
        report_progress(i, NUM_TRAINING_SESSIONS , loss.detach().numpy() )
    # backpropagation
    network.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step(loss)
    

torch.save(network.state_dict(), r"C:\Users\Yannick\Desktop\MA\Programming part\models\quadrat3D.pth")
print("Finished")