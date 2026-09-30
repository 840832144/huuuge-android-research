"""Recover complete NUL-terminated FileDescriptorProto blobs from the current ELF.

Reads static application code only. Ambiguous candidates or missing dependencies fail
closed; an old descriptor is only a required-name reference, never replacement bytes.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import re

from google.protobuf import descriptor_pb2, descriptor_pool
from google.protobuf.message import DecodeError


def varint(data, offset):
    value = 0
    for shift in range(0, 70, 7):
        byte = data[offset]
        offset += 1
        value |= (byte & 127) << shift
        if byte < 128:
            return value, offset
    raise ValueError('Invalid protobuf varint')


def extract(data, required_names):
    if not data.startswith(b'\x7fELF'):
        raise ValueError('Expected the installed native ELF library')
    found = {}
    fields = descriptor_pb2.FileDescriptorProto.DESCRIPTOR.fields_by_number
    for match in re.finditer(rb'\x0a([\x01-\x7f])([A-Za-z0-9_./-]+\.proto)', data):
        if match[1][0] != len(match[2]):
            continue
        start = match.start()
        offset = start
        seen = set()
        try:
            while data[offset] != 0:
                tag, offset = varint(data, offset)
                number, wire = tag >> 3, tag & 7
                field = fields.get(number)
                if field is None or wire not in (0, 2):
                    raise ValueError('Not a complete descriptor boundary')
                if not field.is_repeated and number in seen:
                    raise ValueError('Duplicate singular field')
                seen.add(number)
                size, offset = varint(data, offset)
                if wire == 2:
                    offset += size
                if offset - start > 4 * 1024 * 1024:
                    raise ValueError('Descriptor exceeds bounded size')
            blob = data[start:offset]
            fd = descriptor_pb2.FileDescriptorProto.FromString(blob)
            if not fd.IsInitialized() or fd.name.encode() != match[2] or not (fd.message_type or fd.enum_type or fd.service):
                continue
        except (ValueError, IndexError, DecodeError):
            continue
        if fd.name in found and found[fd.name].SerializeToString() != fd.SerializeToString():
            raise ValueError('Ambiguous embedded descriptor: ' + fd.name)
        found[fd.name] = fd
    if not set(required_names) <= found.keys():
        raise ValueError('Current library is missing required descriptor names')
    pool = descriptor_pool.DescriptorPool()
    pool.AddSerializedFile(descriptor_pb2.DESCRIPTOR.serialized_pb)
    pending = [fd for name, fd in found.items() if name != 'google/protobuf/descriptor.proto']
    while pending:
        remaining = []
        for fd in pending:
            try:
                pool.Add(fd)
            except Exception:
                remaining.append(fd)
        if len(remaining) == len(pending):
            raise ValueError('Current descriptor dependencies do not resolve')
        pending = remaining
    pool.FindMessageTypeByName('Casino.RpcMessage')
    pool.FindFileByName('Services.proto')
    result = descriptor_pb2.FileDescriptorSet()
    for name in sorted(found):
        result.file.add().CopyFrom(found[name])
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--library', type=Path, required=True)
    parser.add_argument('--reference', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    reference = descriptor_pb2.FileDescriptorSet.FromString(args.reference.read_bytes())
    result = extract(args.library.read_bytes(), [fd.name for fd in reference.file])
    with args.out.open('xb') as handle:
        handle.write(result.SerializeToString())
    print('Recovered and dependency-validated %d current descriptor files' % len(result.file))


if __name__ == '__main__':
    main()
