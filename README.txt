Steps to build and execute your system:

1) Download postgres(for mac at http://www.postgresql.org/download/macosx/)
	a) click on the 'Postgress.app' link

2) Install pip: run 'easy_install pip' in the command line

3) Navigate to /GauchoSpace directory and run 'pip install -r requirements.txt'

4) Run the command: 'source virtualenvwrapper.sh'

5) Run the command: 'workon gauchospace'

6) Run the command: 'foreman start'
	a) The terminal will output a few lines. Navigate to 'http://0.0.0.0:5000' in a browser.

7) Homepage will show up. Click on the Log In with Facebook button and authorize the application.

8) When you log in, the site will automatically go to the Offers page, which shows all current offers.

9) You can click on the drop down menu (top right corner) and select Profile to view your own profile.(Not fully implemented but exists)

10) You can click on the SwapBlock option in the drop down menu, which will take you to your own SwapBlock(where you can add classes you wish to trade).(Not fully implemented but exists)

11) To go back to the OfferStream click on GauchoSwap, in the top left corner.

12) You can click logout to log out of the site.
