import torch
scores = torch.tensor([-9.73, -11.03, -10.14])
probabilities = torch.softmax(scores, dim=0)
print(probabilities)