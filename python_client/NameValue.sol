pragma solidity ^0.4.21;

contract NameValue {
  uint[] public keys;
  mapping (uint => string) public data;

  event KeyUpdated(string key, string value);
  event KeyRemoved(string key);

  function update(string key, string value) public {
    uint key_uint = stringToUintHash(key);

    data[key_uint] = value;

    bool exists = false;
    for (uint i=0; i<keys.length; i++) {
      if (keys[i] == key_uint) {
        exists = true;
        break;
      }
    }

    if (! exists) {
      keys.push(key_uint);
    }

    emit KeyUpdated(key, value);
  }

  function stringToUintHash(string str) private pure returns (uint) {
    bytes memory tempEmptyStringTest = bytes(str);
    if (tempEmptyStringTest.length == 0) {
      return 0;
    }

    bytes32 b;
    assembly {
      b := mload(add(str, 32))
    }

    return uint(b);
  }

  function get(string key) public view returns (string) {
    uint key_uint = stringToUintHash(key);
    return data[key_uint];
  }

  function remove(string key) public {
    uint key_uint = stringToUintHash(key);

    delete data[key_uint];
    uint deleteIndex;
    for (uint i=0; i<keys.length; i++) {
      if (keys[i] == key_uint) {
        deleteIndex = i;
        break;
      }
    }
    delete keys[deleteIndex];

    emit KeyRemoved(key);
  }

  function dumpKeys() public view returns (uint[]){
    return keys;
  }
}
