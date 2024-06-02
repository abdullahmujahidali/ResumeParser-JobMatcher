from user.models import Experience, Qualification, Skill, Social


def bulk_create_objects(model, data_list, user):
    if not data_list:
        return
    bulk_create_data = []
    if model == Qualification:
        print("in here qualification: ", data_list)
        bulk_create_data = [
            model(
                user=user,
                university=item.get('university', ''),
                degree=item.get('degree', 'BS'),
                institute=item.get('institute', ''),
                grade_type=item.get('grade_type', '4.0'),
                grade=item.get('grade', 0.0),
                start_year=item.get('start', ''),
                end_year=item.get('end', ''),
                major=item.get('major', '')
            ) for item in data_list
        ]
    elif model == Experience:
        print("in here experience: ", data_list)

        bulk_create_data = [
            model(
                user=user,
                title=item.get('title', ''),
                company=item.get('company', ''),
                start_year=item.get('start', ''),
                end_year=item.get('end', ''),
                description=item.get('description', '')
            ) for item in data_list
        ]
    elif model == Skill:
        print("in here skill: ", data_list)
        bulk_create_data = [
            model(
                user=user,
                name=item
            ) for item in data_list
        ]
    elif model == Social:
        print("in here social: ", data_list)
        bulk_create_data = [
            model(
                user=user,
                url=item
            ) for item in data_list
        ]

    model.objects.bulk_create(bulk_create_data)
