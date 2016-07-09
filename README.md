# enumpy-objc
Simple csv to NS_ENUM converter


###Usage:
```python enum.py --input input.csv --name SomeEnumName```

###Output:
```
enum:
typedef NS_ENUM(NSUInteger, SomeEnumName) {
	SomeEnumNameFirst = 1,
	SomeEnumNameTheSecond,
	SomeEnumNameThirdWithComment, // this is comment
};

transformer dict:
@{
	@"FIRST" : @(SomeEnumNameFirst),
	@"THE_SECOND" : @(SomeEnumNameTheSecond),
	@"THIRD_WITH_COMMENT" : @(SomeEnumNameThirdWithComment),
};
```
