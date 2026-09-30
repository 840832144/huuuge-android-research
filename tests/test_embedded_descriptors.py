"""Static synthetic ELF/descriptor fixtures, never cloud or gameplay evidence."""
import importlib.util
from pathlib import Path
import unittest

from google.protobuf import descriptor_pb2 as pb

spec = importlib.util.spec_from_file_location('extract', Path(__file__).resolve().parents[1] / 'scripts/extract_embedded_descriptors.py')
extractor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(extractor)


def descriptor(method='CurrentMethod'):
    fd = pb.FileDescriptorProto(name='Services.proto', package='Casino', syntax='proto2')
    message = fd.message_type.add(name='RpcMessage')
    message.field.add(name='service_index', number=1, type=5, label=1)
    fd.service.add(name='SlotsGame').method.add(name=method, input_type='.Casino.RpcMessage', output_type='.Casino.RpcMessage')
    return fd


class ExtractionTests(unittest.TestCase):
    def test_current_blob_and_method_order_are_preserved(self):
        current = descriptor()
        current.service[0].method.add(name='Second', input_type='.Casino.RpcMessage', output_type='.Casino.RpcMessage')
        library = b'\x7fELF' + current.SerializeToString() + b'\0padding'
        recovered = extractor.extract(library, ['Services.proto'])
        self.assertEqual(recovered.file[0], current)

    def test_missing_reference_name_is_not_replaced_with_old_schema(self):
        library = b'\x7fELF' + descriptor().SerializeToString() + b'\0'
        with self.assertRaisesRegex(ValueError, 'missing'):
            extractor.extract(library, ['Absent.proto'])

    def test_ambiguous_same_name_is_rejected(self):
        library = b'\x7fELF' + descriptor('First').SerializeToString() + b'\0' + descriptor('Different').SerializeToString() + b'\0'
        with self.assertRaisesRegex(ValueError, 'Ambiguous'):
            extractor.extract(library, ['Services.proto'])

    def test_unresolved_dependencies_are_rejected(self):
        current = descriptor()
        current.dependency.append('Absent.proto')
        with self.assertRaisesRegex(ValueError, 'dependencies'):
            extractor.extract(b'\x7fELF' + current.SerializeToString() + b'\0', ['Services.proto'])


if __name__ == '__main__':
    unittest.main()
