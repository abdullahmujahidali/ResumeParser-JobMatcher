from user.models import Experience, Qualification, Skill, Social


def bulk_create_objects(model, data_list, user):
    if not data_list:
        return
    bulk_create_data = []
    if model == Qualification:
        bulk_create_data = [
            model(
                user=user,
                university=item.get('university', ''),
                degree=item.get('degree', 'BS'),
                institute=item.get('institute', ''),
                grade_type=item.get('grade_type', '4.0'),
                grade=item.get('grade', 0.0),
                start_year=int(item.get('start', 0)),
                end_year=int(item.get('end', 0)),
                major=item.get('major', '')
            ) for item in data_list
        ]
    elif model == Experience:
        bulk_create_data = [
            model(
                user=user,
                title=item.get('title', ''),
                company=item.get('company', ''),
                start_year=int(item.get('start', '').split()
                               [-1]) if item.get('start') else 0,
                end_year=int(item.get('end', '').split(
                )[-1]) if item.get('end') and item.get('end') != 'Present' else None,
                description=item.get('description', '')
            ) for item in data_list
        ]
    elif model == Skill:
        bulk_create_data = [
            model(
                user=user,
                name=item
            ) for item in data_list
        ]
    elif model == Social:
        bulk_create_data = [
            model(
                user=user,
                url=item
            ) for item in data_list
        ]

    model.objects.bulk_create(bulk_create_data)
