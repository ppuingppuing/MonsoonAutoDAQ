LOCAL_PATH	:= $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE	:= DAQDaemon
LOCAL_SRC_FILES	:= DAQDaemon.c

include $(BUILD_EXECUTABLE)
