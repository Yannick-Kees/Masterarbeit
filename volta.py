from loss_functionals import *

####################
# Settings #########
####################

# Neuronal Network
NUM_TRAINING_SESSIONS = 50000
START_LEARNING_RATE = 0.0001
PATIENCE = 1500
NUM_NODES = 512
FOURIER_FEATUERS = True
SIGMA = 5.0
BATCHSIZE = 10000 #16k zu viel

# Phase-Loss
LOSS = "AT"
MONTE_CARLO_SAMPLES = 2000
MONTE_CARLO_BALL_SAMPLES = 60
EPSILON = .0001
if LOSS == "MM":
    CONSTANT = 50.0 if not FOURIER_FEATUERS else 140.0 # 14, Modica Mortola
else:
    # CONSTANT = 40. if FOURIER_FEATUERS else 10.0 # 14, Constante höher bei FF <- FF
    CONSTANT = 40. if FOURIER_FEATUERS else 10.0 # SIREN
MU = 0.5


####################
# Main #############
####################

#experiments = [ 0.01,0.1,.5,1,2,3,4,5,6,7,8,9,10]


network = ParkEtAl(3, [512]*3 , [], FourierFeatures=FOURIER_FEATUERS, num_features = 8, sigma = SIGMA )
#network =  Siren(3,2,512,1)
network.to(device) 
optimizer = optim.Adam(network.parameters(), START_LEARNING_RATE )
scheduler = ReduceLROnPlateau(optimizer, 'min', patience=PATIENCE, verbose=False)

file = open("3dObjects/bunny_0.ply")
pc = read_ply_file(file)
cloud = torch.tensor( normalize(pc))
#cloud = torch.tensor( flat_circle(2000) )

# Activate for the bunny
cloud += torch.tensor([0.15,-.15,.1]).repeat(cloud.shape[0],1)
cloud = torch.tensor(normalize(cloud) )

#cloud = torch.tensor(normalize(experiments[l] ))


pc = Variable( cloud , requires_grad=True).to(device)
use_batch = (len(pc) > BATCHSIZE )

for i in range(NUM_TRAINING_SESSIONS+1):
    # training the network
    # feed forward
    # Omega = [0,1]^2
    
    network.zero_grad()
    
    if use_batch:
        
        indices = np.random.choice(len(pc), BATCHSIZE, False)
        pointcloud = pc[indices]
    else:
        pointcloud = pc
    #for _ in range(2):
    if LOSS == "AT":
        loss = .5 * AT_loss(network, pointcloud, EPSILON, MONTE_CARLO_SAMPLES, MONTE_CARLO_BALL_SAMPLES, CONSTANT )
        if (i%50==0):
            report_progress(i, NUM_TRAINING_SESSIONS , loss.detach().cpu().numpy() )
    else:
        loss = Phase_loss(network, pointcloud, EPSILON, MONTE_CARLO_SAMPLES, MONTE_CARLO_BALL_SAMPLES, CONSTANT, MU)
        if (i%10==0):
            report_progress(i, NUM_TRAINING_SESSIONS , loss.detach().cpu().numpy() )
        # report_progress(i, NUM_TRAINING_SESSIONS , loss.detach().cpu().numpy() )
        
        # backpropagation
        
        loss.backward(retain_graph= True )
    optimizer.step()
    scheduler.step(loss)
    
indices = np.random.choice(len(pc), BATCHSIZE, False)
pointcloud = pc[indices]
print("Loss: ", torch.abs(network(pointcloud)).mean())
torch.save(network.state_dict(), "cube.pth")
toParaview(network, 256, 0)
print("Finished")

