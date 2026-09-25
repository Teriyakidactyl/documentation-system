from __future__ import annotations

from pathlib import Path
import sys
import unittest

SOFTWARE=Path(__file__).resolve().parents[1]
if str(SOFTWARE) not in sys.path:
    sys.path.insert(0,str(SOFTWARE))

from core import ExpectedFailure, Failure, Field, InputSchema, Operation, Result, Source, invoke

class CoreContractTests(unittest.TestCase):
    def test_schema_failure_is_canonical_and_source_addressable(self) -> None:
        owner=Source("test.operation","test.py","handler")
        operation=Operation(
            id="test.required",commands=(("test","required"),),owner=owner,
            input_schema=InputSchema((Field("name","string"),)),
            handler=lambda inputs: Result.success(inputs),
        )
        result=invoke(operation,{})
        self.assertFalse(result.ok)
        self.assertEqual("INVALID_INPUT",result.failures[0].name)
        self.assertEqual(owner,result.failures[0].origin)
        self.assertEqual(("test.required",),result.failures[0].provenance)

    def test_recognized_origin_survives_operation_propagation(self) -> None:
        owner=Source("test.operation","operation.py","handler")
        origin=Source("test.capability","capability.py","parse")
        def handler(inputs):
            raise ExpectedFailure(Failure(
                origin=origin,name="BROKEN",classification="malformed",
                subject={"value":inputs["value"]},message="broken",
                provenance=("capability.parse",),
            ))
        operation=Operation(
            id="test.propagate",commands=(("test","required"),),owner=owner,
            input_schema=InputSchema((Field("value","string"),)),handler=handler,
        )
        result=invoke(operation,{"value":"x"})
        self.assertEqual(origin,result.failures[0].origin)
        self.assertEqual(("capability.parse","test.propagate"),result.failures[0].provenance)

    def test_unexpected_exception_converts_once_at_operation_boundary(self) -> None:
        owner=Source("test.operation","operation.py","handler")
        def handler(inputs):
            raise RuntimeError("boom")
        operation=Operation(
            id="test.internal",commands=(("test","required"),),owner=owner,
            input_schema=InputSchema(),handler=handler,
        )
        result=invoke(operation,{})
        self.assertEqual("INTERNAL",result.failures[0].name)
        self.assertEqual(owner,result.failures[0].origin)

if __name__=="__main__":
    unittest.main()
