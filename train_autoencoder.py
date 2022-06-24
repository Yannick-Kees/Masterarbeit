#from chamfer_distance import ChamferDistance
from shapemaker import *
from pytorch3d.loss import (
    chamfer_distance, 
    mesh_edge_loss, 
    mesh_laplacian_smoothing, 
    mesh_normal_consistency,
)

NUM_TRAINING_SESSIONS = 2
num_points = 10
Batch_size = 4

autoencoder = PCAutoEncoder(3, num_points)



optimizer = optim.Adam(autoencoder.parameters(), lr=0.001, betas=(0.9, 0.999))
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=20, gamma=0.5)


for epoch in range(NUM_TRAINING_SESSIONS+1):

    points = []
    for _ in range(Batch_size):
        points.append(np.array(shape_maker1(3,num_points)).T)
    # points = points.cuda()
    points = Variable( Tensor(points) , requires_grad=True).to(device)

    optimizer.zero_grad()
    reconstructed_points, global_feat = autoencoder(points)

    dist1, dist2 = chamfer_distance(points, reconstructed_points)

    train_loss = torch.mean(dist1)

    # Calculate the gradients using Back Propogation
    train_loss.backward() 

    # Update the weights and biases 
    optimizer.step()
    if epoch % 50 == 0:
        report_progress(epoch, NUM_TRAINING_SESSIONS , train_loss.detach().cpu().numpy() )
    if epoch % 10000 == 0:
        torch.save(autoencoder.state_dict(), 'autoencoder.pth')
        

    scheduler.step()

torch.save(autoencoder.state_dict(), 'autoencoder.pth')

print("Finished")
    
    
    
        
