def rotate_axis(x, add_angle=0, axis=1):
    import torch
    
    
    axes = list(range(3))
    axes.remove(axis)
    ax1, ax2 = axes
    angle = torch.atan2(x[..., ax1], x[..., ax2])
    if isinstance(add_angle, torch.Tensor):
        while add_angle.ndim < angle.ndim:
           add_angle = add_angle.unsqueeze(-1)
    angle = angle + add_angle
    dist = x.norm(dim=-1)
    t = []
    _, t = zip(*sorted([
        (axis, x[..., axis]),
        (ax1, torch.sin(angle) * dist),
        (ax2, torch.cos(angle) * dist),
    ]))
    return torch.stack(t, dim=-1)
