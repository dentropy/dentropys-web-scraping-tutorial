import os

from pywebcopy import save_webpage
save_webpage(
      url="http://wikipedia.com/",
      project_folder=os.getcwd(),
      project_name="wikipedia",
      bypass_robots=True,
      debug=True,
      open_in_browser=True,
      delay=None,
      threaded=False,
)