pragma solidity ^0.4.24;

contract NameValue {
  uint[] public keys;
  mapping (uint => string) public data;

  event KeyUpdated(string key, string value);
  event KeyRemoved(string key);

  function update(string key, string value) public {
    uint key_uint = stringToUint(key);

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

  function stringToUint(string str) private pure returns (uint result) {
    bytes memory b = bytes(str);
    uint i;
    result = 0;
    for (i = 0; i < b.length; i++) {
      uint c = uint(b[i]);
      if (c >= 48 && c <= 57) {
        result = result * 10 + (c - 48);
      }
    }
  }

  function get(string key) public view returns (string) {
    uint key_uint = stringToUint(key);
    return data[key_uint];
  }

  function remove(string key) public {
    uint key_uint = stringToUint(key);

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

  function getFromUint(uint key_uint) public view returns (string) {
    return data[key_uint];
  }

}
