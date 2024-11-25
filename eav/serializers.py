import logging

from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from eav.models import Attribute, EnumGroup, EnumValue, Value

logger = logging.getLogger(__name__)


class EavEntitySerializer(serializers.ModelSerializer):
    attribute = serializers.CharField(source="attribute.slug")
    value = serializers.CharField()

    class Meta:
        model = EnumValue
        fields = ["attribute", "value"]

    def update_or_create(self, validated_data):
        """
        Updates or creates an attribute and its associated value based on the provided validated data.

        Args:
            validated_data (dict): A dictionary containing the following keys:
                - attribute (str): The slug of the attribute.
                - value (str): The value to be associated with the attribute.
                - entity (Model): The entity to which the attribute and value are related.

        Returns:
            Value: The created or updated Value instance.

        Raises:
            serializers.ValidationError: If the enum group is not found for the attribute.
        """
        attribute_slug = validated_data.get("attribute")
        value_data = validated_data.get("value")
        entity = validated_data.get("entity")
        try:
            attribute = Attribute.objects.get(
                slug=attribute_slug,
            )
            logger.debug(f"Attribute exists: {attribute}")

            enum_group = attribute.enum_group

            if enum_group:
                enum_value, created = EnumValue.objects.get_or_create(
                    value=value_data,
                )
                enum_group.values.add(enum_value)

                value, created = Value.objects.get_or_create(
                    attribute=attribute,
                    entity_ct=ContentType.objects.get_for_model(entity),
                    entity_id=entity.id,
                )
                value.value_enum = enum_value
                value.save()
                if created:
                    logger.debug(f"Value created: {value}")
                else:
                    logger.debug(f"Value exists: {value}")

                return value
        except Attribute.DoesNotExist:
            logger.debug(f"Attribute does not exist: {attribute_slug}")
            enum_group, created = EnumGroup.objects.get_or_create(name=attribute_slug)
            attribute = Attribute.objects.create(
                slug=attribute_slug,
                name=attribute_slug,
                datatype=Attribute.TYPE_ENUM,
                enum_group=enum_group,
            )

            enum_value, created = EnumValue.objects.get_or_create(
                value=value_data,
            )
            enum_group.values.add(enum_value)

            value, created = Value.objects.get_or_create(
                attribute=attribute,
                entity_ct=ContentType.objects.get_for_model(entity),
                entity_id=entity.id,
            )
            value.value_enum = enum_value
            if created:
                logger.debug(f"Value created: {value}")
            else:
                logger.debug(f"Value exists: {value}")

            return value
        else:
            raise serializers.ValidationError("Enum group not found for the attribute.")

    # def update_or_create(self, validated_data):
    #     attribute_slug = validated_data.get("attribute")
    #     value_data = validated_data.get("value")
    #     attribute, _ = Attribute.objects.get_or_create(
    #         slug=attribute_slug,
    #         defaults={
    #             "name": attribute_slug,
    #             "datatype": Attribute.TYPE_ENUM,  # Ensure this matches your datatype
    #         },
    #     )
    #     enum_group = attribute.enum_group

    #     if enum_group:
    #         enum_value, created = EnumValue.objects.update_or_create(
    #             value=value_data,
    #         )
    #         enum_group.values.add(enum_value)

    #         value = Value.objects.create(
    #             attribute=attribute,
    #             value_enum=enum_value,
    #             entity_ct=ContentType.objects.get_for_model(entity),
    #             entity_id=entity.id,
    #         )
    #         return value
    #     else:
    #         raise serializers.ValidationError("Enum group not found for the attribute.")


class EnumValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnumValue
        fields = "__all__"


class EnumGroupSerializer(serializers.ModelSerializer):
    values = EnumValueSerializer(many=True, required=False)

    class Meta:
        model = EnumGroup
        fields = "__all__"

    # def create(self, validated_data):
    #     values_data = validated_data.pop("values")
    #     enum_group = EnumGroup.objects.create(**validated_data)
    #     for value_data in values_data:
    #         EnumValue.objects.update_or_create(
    #             enum_group=enum_group, value=value_data["value"], defaults=value_data
    #         )
    #     return enum_group

    # def update(self, instance, validated_data):
    #     values_data = validated_data.pop("values")
    #     instance.name = validated_data.get("name", instance.name)
    #     instance.save()

    #     for value_data in values_data:
    #         EnumValue.objects.update_or_create(
    #             enum_group=instance, value=value_data["value"], defaults=value_data
    #         )
    #     return instance


class AttributeSerializer(serializers.ModelSerializer):
    enum_group = EnumGroupSerializer(required=False)
    datatype = serializers.CharField(required=False)
    slug = serializers.SlugField(required=False)
    choices = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Attribute
        fields = "__all__"

    def create(self, validated_data):
        name = validated_data.pop("name", None)
        choices = validated_data.pop("choices", [])
        # values = []
        choices_group, created = EnumGroup.objects.get_or_create(name=name)

        for choice in choices:
            value, created = EnumValue.objects.get_or_create(value=choice)
            # value = EnumValue.objects.create(value=choice)
            # values.append(value)
            # value = None

            choices_group.values.add(value)

        attribute, created = Attribute.objects.get_or_create(
            name=name,
            # slug=slugify.slugify(name),
            datatype=Attribute.TYPE_ENUM,
            enum_group=choices_group,
        )

        return attribute

    #     attribute = Attribute.objects.create(**validated_data)
    #     if enum_group_data:
    #         enum_group_serializer = EnumGroupSerializer(data=enum_group_data)
    #         if enum_group_serializer.is_valid():
    #             enum_group = enum_group_serializer.save()
    #             attribute.enum_group = enum_group
    #             attribute.save()
    #     return attribute

    # def update(self, instance, validated_data):
    #     enum_group_data = validated_data.pop("enum_group", None)
    #     attribute = super().update(instance, validated_data)
    #     if enum_group_data:
    #         enum_group_serializer = EnumGroupSerializer(
    #             instance.enum_group, data=enum_group_data
    #         )
    #         if enum_group_serializer.is_valid():
    #             enum_group_serializer.save()
    #     return attribute


class ModelEavSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    eav = serializers.ListField(child=EavEntitySerializer(), required=False)

    class Meta:
        model = None
        fields = "__all__"

    def create(self, validated_data):
        eav_data = validated_data.pop("eav", [])
        example_model = self.Meta.model.objects.create(**validated_data)
        for eav_item in eav_data:
            value = EavEntitySerializer().update_or_create(
                {
                    "attribute": eav_item["attribute"],  # ["slug"],
                    "value": eav_item["value"],
                    "entity": example_model,
                },
            )
            value.entity = example_model
            value.save()
        return example_model

    def update(self, instance, validated_data):
        # TODO: separate both parsing depending on the serializer
        eav_data = validated_data.pop("eav", [])
        instance = super().update(instance, validated_data)
        for attribute, value in eav_data:
            value = EavEntitySerializer().update_or_create(
                {
                    # "attribute": eav_item["attribute"],  # ["slug"],
                    # "value": eav_item["value"],
                    "attribute": attribute,
                    "value": value,
                    "entity": instance,
                },
            )
            value.entity = instance
            value.save()

        return instance


class ModelEavDictSerializer(ModelEavSerializer):
    class Meta(ModelEavSerializer.Meta):
        fields = "__all__"

    def to_internal_value(self, data):
        eav_data = data.pop("eav", {})
        internal_value = super().to_internal_value(data)
        internal_value["eav"] = eav_data
        return internal_value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        eav_representation = {}
        for eav_item in instance.eav_values.all():
            eav_representation[eav_item.attribute.slug] = eav_item.value_enum.value
        representation["eav"] = eav_representation
        return representation
