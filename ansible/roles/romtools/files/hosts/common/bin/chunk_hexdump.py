#!/usr/bin/env python3

import os
import re
import sys

class FileReader:
    def __init__(self, filename):
        self.__BUFFER_SIZE = 4 * 2**10

        self.file_handle = open(filename, 'rb')
        self.raw_pointer = 0
        self.raw_buffer = []

        self.buffer = []
        self.held_character = None

    def peek(self, consume=False):
        """
        Peek at the next character. Multiple calls to peek(False) will always return the same character.

        Use peek(True) to consume the character. peek(True) is the same as read().
        """
        if self.held_character == None:
            self.held_character = self.__nextByte()

        c = self.held_character

        if consume:
            self.held_character = None

        return c

    def read(self):
        c = self.peek(True)
        return c

    def __ingestData(self):
        if self.raw_pointer < 0:
            return

        if self.raw_pointer >= len(self.raw_buffer):
            self.raw_buffer = self.file_handle.read(self.__BUFFER_SIZE)

            if len(self.raw_buffer) < 1:
                # EOF
                self.raw_pointer = -1
            else:
                self.raw_pointer = 0

    def __nextByte(self):
        self.__ingestData()

        if self.raw_pointer < 0:
            return b''

        # Because we are dereferencing a byte array, simply
        #  getting the index will return an int
        #  to get a byte, we need to use a range
        mybyte = self.raw_buffer[self.raw_pointer:self.raw_pointer+1]
        self.raw_pointer += 1

        return mybyte

    def byteString(self, reset_buffer):
        data = b''.join(self.buffer)

        if reset_buffer:
            self.buffer = []

        return data

    def close(self):
        self.file_handle.close()

    def readUntil(self, edgebytes=[b'\x0a', b'\x0d', b'\x00']):
        mybyte = None

        while True:
            mybyte = self.read()

            if mybyte == b'':
                return self.byteString(True)

            self.buffer.append(mybyte)

            if mybyte in edgebytes:
                while self.peek() in edgebytes:
                    self.buffer.append(self.read() )

                return self.byteString(True)

class BytesPrinter:
    def __init__(self, width=32):
        assert width % 2 == 0, "Width must be a multiple of two"
        self.__width = width
        self.__to_process = b''
        self.__chunk = b''


    def __chomp(self):
        # Chop half the width - each byte expands to two in
        # ASCII representation
        h_width = self.__width // 2
        self.__chunk = self.__to_process[:h_width]
        self.__to_process = self.__to_process[h_width:]

        return len(self.__chunk) > 0


    def __chunkString(self):
        chars = []
        for i in self.__chunk: # Iterating bytes converts to int
            if i < 32 or i >126:
                chars.append('.')
            else:
                chars.append(chr(i))
        return ''.join(chars)


    def __getChunkPadding(self, padding):
        chunk_length = len(self.__chunk)
        return padding * (self.__width - chunk_length)


    def get_formatted_lines(self, data_bytes):
        self.__to_process = data_bytes
        bar = '|'
        lines = []
        
        while self.__chomp():
            spaced = " ".join(re.findall("..", str(self.__chunk.hex())))
            formatted = spaced.ljust(self.__width + self.__width//2-1)
            cleansed = self.__chunkString().ljust(self.__width)
            lines.append(f"{bar} {formatted}  {bar}  {cleansed} {bar}")

            # Actually appears in case of multiline chunk
            bar=':'

        return lines


    def print(self, data_bytes):
        lines = self.get_formatted_lines(data_bytes)
        lines = os.linesep.join(lines)
        print(lines)


def getChunks(filename):
    fr = FileReader(filename)

    while True:
        chunk_bytes = fr.readUntil()

        if len(chunk_bytes) < 1:
            break

        yield chunk_bytes

    fr.close()


def main(args):
    bp = BytesPrinter()

    for filename in args:
        for chunk in getChunks(filename):
            if chunk:
                bp.print(chunk)
            else:
                break


if __name__ == "__main__":
    main(sys.argv[1:])
