import datetime
import os
import asyncio
import logging

class FileHandler:
    def __init__(self,createnewfiles=True, useuserinput=False, enablelogging=True, encoding='utf-8'):


        # Booleans
        self.useUserInput = useuserinput
        self.isLogging = enablelogging
        self.createNewFiles = createnewfiles

        # Counters
        self.fileCount = 0
        self.numLines = 0

        # File Names
        self.file = None
        self.newFile = None

        # Data
        self.data = None
        self.dataList = None

        # Misc.
        self.encoding = encoding
        self.executionStartTime = None
        self.endTime = None
        now = datetime.datetime.now()

        # Starts the logger
        if self.isLogging:
            dateTime = now.strftime("%Y-%m-%d %H.%M.%S")
            logFile = "Datalogs/Darklai Log " + dateTime + ".log"
            logging.basicConfig(filename=logFile, level=logging.INFO)
            logging.info('Class: Filehandler has been initialized. ' + str(dateTime))

    # Reads the file, and puts each line into a list
    # Throws an exception if the file name is invalid.
    async def get_file_contents(self, datafile):
        await self.log_message('Attempting to get the file contents from ' + str(datafile), 1)
        try:
            # Open the file for reading,
            # And read each line into a new list for the dataList list.
            with open(datafile, 'r') as file:
                self.dataList = [line.rstrip('\n') for line in file]
                file.close()

            # For every line in the data, replace \t with a space,
            # And \n with a space.
            for i in range(0, len(self.dataList)):
                self.dataList[i] = self.dataList[i].replace('\t', ' ')
                self.dataList[i] = self.dataList[i].replace('\n', ' ')
            await self.log_message('File contents retrieved from ' + str(datafile) + ' successfully!', 1)
            return self.dataList

        # Handle any exceptions
        except Exception:
            await self.log_message('File ' + str(datafile) + ' does not exist, or is invalid.', 3)
            return


    # Appends data to a new or existing text file.
    # Throws an exception if the file name or data is invalid.
    async def append_to_file(self, data, file):
        await self.log_message('Attempting to append to file ' + str(file), 1)
        # Overwrite the file and data variables to match the arguments.
        self.file = file
        self.data = data

        try:
            # If createNewFiles is disabled, and the file exists
            if self.createNewFiles == False and os.path.isfile(self.file):
                # Open the file for appending.
                with open(self.file, 'a+', encoding=self.encoding) as file:
                    # If the number of lines is not 0, make a new line before writing
                    if self.numLines != 0:
                        file.write('\n')
                    # Write the data to the file.
                    file.write(str(self.data))
                    file.close()
                await self.log_message('The file ' + str(file) + ' was appended to successfully!', 1)
                # Add to the numLines counter.
                self.numLines += 1
                return

            # If createNewFiles is enabled, and the file does not exist
            elif self.createNewFiles and os.path.isfile(self.file) == False:
                # Create a new file, and write the data to it.
                with open(self.file, 'w+', encoding=self.encoding) as file:
                    # If the number of lines is not 0, make a new line before writing
                    if self.numLines != 0:
                        file.write('\n')
                    # Write the data to the file.
                    file.write(str(self.data))
                    file.close()
                await self.log_message('The file ' + str(file) + ' was appended to successfully!', 1)
                # Add to the numLines counter.
                self.numLines += 1
                self.fileCount += 1
                return

            # If createNewFiles is enabled, and the file exists
            elif self.createNewFiles and os.path.isfile(self.file):
                # Open the file for appending.
                with open(self.file, 'a+', encoding=self.encoding) as file:
                    # If the number of lines is not 0, make a new line before writing
                    if self.numLines != 0:
                        file.write('\n')
                    file.write(str(self.data))
                    file.close()
                await self.log_message('The file ' + str(file) + ' was appended to successfully!', 1)
                # Add to the numLines counter.
                self.numLines += 1
                return

            # Else, do not do anything.
            else:
                await self.log_message(
                    'file ' + str(file) + ' was not created, because variable createNewFiles was set to false!', 2)
                return

        # Handle any exceptions
        except Exception:
            await self.log_message('File or data defined does not exist, or is invalid!', 3)
            # Close the file, just in case an exception occured while the file was still open
            file.close()
            return


    # Overwrites to a new or existing file.
    # Throws an exception if the file name or data is invalid.
    async def overwrite_file(self, data, file):
        await self.log_message('Attempting to overwrite the file ' + str(file), 1)
        # Overwrite the file and data variables to match the arguments.
        self.file = file
        self.data = data

        try:
            # If createNewFiles is disabled, and the file exists
            if self.createNewFiles == False and os.path.isfile(self.file):
                # Open the file for writing.
                with open(self.file, 'w', encoding=self.encoding) as file:
                    file.write(str(self.data))
                    file.close()
                await self.log_message('The file ' + str(file) + ' was written to successfully!', 1)
                return

            # If createNewFiles is enabled, and the file does not exist
            elif self.createNewFiles and os.path.isfile(self.file) == False:
                # Create the file for writing.
                with open(self.file, 'w', encoding=self.encoding) as file:
                    file.write(str(self.data))
                    file.close()
                await self.log_message('The file ' + str(file) + ' was written to successfully!', 1)
                self.fileCount += 1
                return

            # If createNewFiles is enabled, and the file exists
            elif self.createNewFiles and os.path.isfile(self.file):
                # Open the file for writing.
                with open(self.file, 'w', encoding=self.encoding) as file:
                    file.write(str(self.data))
                    file.close()
                await self.log_message('The file ' + str(file) + ' was written to successfully!', 1)
                return

            # Else do nothing.
            else:
                await self.log_message(
                    'file ' + str(file) + ' was not created, because variable createNewFiles was set to false!', 2)
                return

        # Handle any exceptions
        except Exception:
            await self.log_message('File ' + str(file) + ' or data defined does not exist, or is invalid!', 3)
            # Close the file, just in case an exception occured while the file was still open
            file.close()
            return


    # Creates a new file for the user.
    # Currently does not throw any exceptions
    async def create_new_file(self, file):
        # Overwrite the newFile variable to match the arguments.
        self.newFile = file
        # Initialize the local counter
        counter = 0
        await self.log_message('Attempting to create new file ' + str(self.newFile), 1)

        # While the file exists
        while os.path.isfile(self.newFile):
            await self.log_message('There is a file that exists when trying to create ' + str(file) + '!', 2)

            # If user input is enabled
            if self.useUserInput:
                # Ask for the user to name the file until a new file name is found
                await self.log_message('Asking for the user to input another file name', 1)
                self.file = input('sorry,that file already exists! Please type another file name \n')

            # Else, generate a name for the file.
            else:
                await self.log_message('Appending a number to the original file name.', 1)
                counter += 1
                # If the counter is equal to 1
                if counter == 1:
                    # Split apart the file name from the file extension, and save it as a list.
                    splitFile = os.path.splitext(self.newFile)
                    # Add the count number into the new file name.
                    self.newFile = splitFile[0] + str(counter) + splitFile[1]

                else:
                    # Add the count number into the new file name.
                    self.newFile = splitFile[0] + str(counter) + splitFile[1]

        # If it is not already an existing file
        if not os.path.isfile(self.newFile):
            await self.log_message('Creating new file ' + str(file), 1)

            # Create a new file with the new file name.
            with open(self.newFile, 'a+', encoding=self.encoding) as file:
                file.write('')
                file.close()
            await self.log_message('New file ' + str(self.newFile) + ' was created successfully', 1)
            self.fileCount += 1
        return

    async def log_message(self, message, level):

        try:
            # If isLogging is set to true
            if self.isLogging:
                # Define all of the local variables
                now = datetime.datetime.now()
                dateTime = now.isoformat()

                # If the level is set to 0, it is a debug message
                if level == 0:
                    logging.debug("{" + str(message) + 'TIME: ' + str(dateTime) + "}")

                # If the level is set to 1, it is a info message
                elif level == 1:
                    logging.info("{" + str(message) + 'TIME: ' + str(dateTime) + "}")

                # If the level is set to 2, it is a warning message
                elif level == 2:
                    logging.warning("{" + str(message) + 'TIME: ' + str(dateTime) + "}")

                # If the level is set to 3, it is a error message
                elif level == 3:
                    logging.error("{" + str(message) + 'TIME: ' + str(dateTime) + "}")

                # If the level is set to 4, it is a critical message
                elif level == 4:
                    logging.critical("{" + str(message) + 'TIME: ' + str(dateTime) + "}")

        # Handle any exceptions
        except Exception:
            # If isLogging is set to true
            if self.isLogging:
                # Define all of the local variables
                now = datetime.datetime.now()
                dateTime = now.isoformat()
                logging.critical('Message inputted for the log was invalid! TIME: ' + str(dateTime))

            # Else, print out a error
            else:
                # Define all of the local variables
                now = datetime.datetime.now()
                dateTime = now.isoformat()
                print('ERROR: LOGGER CANNOT OUTPUT A CERTAIN MESSAGE. TIME: ' + str(dateTime))
        # Define the endTime variable
        now = datetime.datetime.now()
        self.endTime = now
        return