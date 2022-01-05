def save_video(frames, out_path="video.mp4", fps=30, display=False):
    # frames: List[PIL.Image]
    from subprocess import Popen, PIPE
    if display:
        from tqdm.auto import tqdm
        tq = tqdm
    else:
        tq = lambda x: x
    p = Popen(['ffmpeg', '-y', '-f', 'image2pipe', '-vcodec', 'png', '-r', str(fps), '-i', '-', '-vcodec', 'libx264', '-r', str(fps), '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'veryslow', out_path], stdin=PIPE)
    for im in tq(frames):
        im.save(p.stdin, 'PNG')
    p.stdin.close()
    p.wait()
    if display:
        return show_video(out_path, frames[-1].size[0] if frames else None)


def save_gif(frames, out_path="video.mp4", display=False):
    # frames: Iterable[PIL.Image]
    from skvideo.io import FFmpegWriter
    import numpy as np
    if display:
        from tqdm.auto import tqdm
        tq = tqdm
    else:
        tq = lambda x: x
    writer = FFmpegWriter(out_path)
    for frame in tq(frames):
        writer.writeFrame(np.asarray(frame))
        if display:
            from IPython.display import display as show
            show(frame)
    writer.close()
      

def show_video(video_path, width=None, format="video/mp4"):
    if width is None:
        width = 256
    from IPython.display import display, HTML
    from base64 import b64encode
    video = open(video_path, "rb").read()
    data_url = f"data:{format};base64," + b64encode(video).decode()
    return display(HTML(f"""
    <video width={width} controls>
          <source src="{data_url}" type="{format}">
    </video>"""))

  
def cv2_loop(callback=None, loop=None, window_name="window"):
    import cv2

    
    if callback is None:
        def callback(ev, x, y, flags, param):
            if ev == cv2.EVENT_LBUTTONDOWN:
                pass
            if ev == cv2.EVENT_LBUTTONUP:
                pass

    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, callback)
    while True:
        ret, frame = cap.read()
        if loop is not None:
            new_frame = loop(frame)
            if new_frame is not None:
                frame = new_frame
        cv2.imshow(window_name, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyWindow(window_name)
