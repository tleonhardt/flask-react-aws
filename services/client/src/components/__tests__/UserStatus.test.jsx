import React from 'react';
import { render, cleanup, wait } from '@testing-library/react';
import axios from 'axios';

import UserStatus from '../UserStatus';

afterEach(cleanup);

jest.mock("axios");

it('renders properly when authenticated', async() => {
  axios.mockImplementationOnce(() =>
    Promise.resolve({
      data: { email: 'test@test.com', username: 'test' }
    })
  );
  const { container, findByTestId } = render(<UserStatus />);
  await wait(() => {
    expect(axios).toHaveBeenCalledTimes(1);
  });
  expect((await findByTestId('user-email')).innerHTML).toBe('test@test.com');
  expect((await findByTestId('user-username')).innerHTML).toBe('test');
});
