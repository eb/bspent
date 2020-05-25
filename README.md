Small tool to switch the entity list in Quake .bsp files.

Example usage:
```
./bspent.py extract aerowalk.bsp aerowalk.ent
cat aerowalk.ent | sed 's/item_armor1/item_armorInv/g' > aerowank.ent
./bspent.py switch aerowalk.bsp aerowank.ent aerowank.bsp
```

This will create a map called aerowank.bsp that's exactly like aerowalk,
but all green armors are changed to red armors.
