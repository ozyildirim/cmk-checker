import datetime


class Logger:

    def __init__(self):
        self.log_txt_file = open("log_txt_file.txt", "w")
        self.log_txt_file.write("*****CMK-Checker Analyze Tool v1*****\n")
        self.log_txt_file.write(
            "*****" + str(datetime.datetime.now()) + "*****")

    def log_results(self, message):
        print("RESULT LOG: " + message)
        self.log_txt_file.write("\nRESULT LOG:   " + message)

    def log_error(self, message):
        # print("ERROR LOG:  " + message)
        self.log_txt_file.write("\nERROR LOG:    " + message)

    def log_smell(self, message):
        # print("SMELL LOG:  " + message)
        self.log_txt_file.write("\nSMELL LOG:    " + message)

    def log_warning(self, message):
        # print("WARNING LOG:" + message)
        self.log_txt_file.write("\nWARNING LOG:  " + message)

    def log_process(self, message):
        # print("PROCESS LOG:" + message)
        self.log_txt_file.write("\nPROCESS LOG:  " + message)

    def log_report(self, message):
        # print("REPORT LOG: " + message)
        self.log_txt_file.write("\nREPORT LOG:   " + message)

    def close_txt(self):
        self.log_txt_file.close()